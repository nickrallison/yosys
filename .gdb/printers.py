import gdb
import gdb.printing
import sys
from collections import OrderedDict

# /usr/share/gcc/python/libstdcxx/v6/printers.py
sys.path.insert(0, '/usr/share/gcc/python')
from libstdcxx.v6.printers import register_libstdcxx_printers
register_libstdcxx_printers (None)


class VectorPrinter(gdb.ValuePrinter):
    def __init__(self, value):
        self._error = None
        self._size = self._capacity = 0
        element_type = value.type.strip_typedefs().template_argument(0)
        self._is_bool = element_type.code == gdb.TYPE_CODE_BOOL
        try:
            impl = value["_M_impl"]
            self._start = impl["_M_start"]
            finish = impl["_M_finish"]
            end = int(impl["_M_end_of_storage"])
            self._bit_offset = 0
            if self._is_bool:
                self._bit_offset = int(self._start["_M_offset"])
                finish_offset = int(finish["_M_offset"])
                self._start = self._start["_M_p"]
                finish = finish["_M_p"]
            start, finish = int(self._start), int(finish)
            stride = self._start.type.strip_typedefs().target().sizeof
            # Locals can be visible before their constructors have run.
            if (not start and end) or not start <= finish <= end:
                raise gdb.error("invalid or uninitialized storage")
            if (finish - start) % stride or (end - start) % stride:
                raise gdb.error("invalid storage alignment")
            self._size = (finish - start) // stride
            self._capacity = (end - start) // stride
            if self._is_bool:
                self._word_bits = 8 * stride
                if not (0 <= self._bit_offset < self._word_bits and
                        0 <= finish_offset < self._word_bits):
                    raise gdb.error("invalid bit offsets")
                self._size = self._size * self._word_bits + finish_offset - self._bit_offset
                self._capacity = self._capacity * self._word_bits - self._bit_offset
                if not 0 <= self._size <= self._capacity:
                    raise gdb.error("invalid or uninitialized storage")
        except gdb.error as error:
            self._error = str(error)
            self._size = 0

    def display_hint(self):
        return "array"

    def to_string(self):
        if self._error is not None:
            return f"<std::vector: {self._error}>"
        name = "std::vector<bool>" if self._is_bool else "std::vector"
        return f"{name} of length {self._size}, capacity {self._capacity}"

    def num_children(self):
        # DAP otherwise materializes children() just to count a collapsed vector.
        return self._size

    def child(self, n):
        if n < 0 or n >= self._size:
            raise IndexError(n)
        if self._is_bool:
            word, bit = divmod(n + self._bit_offset, self._word_bits)
            value = bool((self._start + word).dereference() & (1 << bit))
        else:
            value = (self._start + n).dereference()
        return (f"[{n}]", value)

    def children(self):
        for n in range(self._size):
            yield self.child(n)


_calling = False
_id_cache = OrderedDict()


if "clear_id_cache" in globals():
    for event in (gdb.events.cont, gdb.events.exited, gdb.events.new_objfile):
        event.disconnect(clear_id_cache)


def clear_id_cache(event):
    if not _calling:
        _id_cache.clear()


for event in (gdb.events.cont, gdb.events.exited, gdb.events.new_objfile):
    event.connect(clear_id_cache)


def call_method(value, method):
    global _calling
    if _calling or value.address is None:
        raise gdb.error("inferior call unavailable")

    # GDB's DAP adapter emits continued/stopped for inferior calls. Zed
    # refreshes variables on stopped, which otherwise calls us forever.
    dap_events = sys.modules.get("gdb.dap.events")
    dap_handler = getattr(dap_events, "_on_inferior_call", None)
    if dap_handler is not None:
        gdb.events.inferior_call.disconnect(dap_handler)

    try:
        _calling = True
        address = int(value.address)
        value_type = value.type.strip_typedefs().unqualified()
        return gdb.parse_and_eval(
            f"((const '{value_type}' *)0x{address:x})->{method}"
        )
    finally:
        _calling = False
        if dap_handler is not None:
            gdb.events.inferior_call.connect(dap_handler)


class IdStringPrinter:
    def __init__(self, value):
        self.value = value

    def display_hint(self):
        return "string"

    def to_string(self):
        index = int(self.value["index_"])
        key = (gdb.selected_inferior().num, index)
        if key in _id_cache:
            _id_cache.move_to_end(key)
            return _id_cache[key]
        if _calling or self.value.address is None:
            return f"<IdString index={index}>"

        try:
            result = call_method(self.value, "c_str()")
            text = result.string(errors="replace")
            # Bound retained strings without limiting the displayed value.
            if len(text) <= 4096:
                _id_cache[key] = text
                if len(_id_cache) > 4096:
                    _id_cache.popitem(last=False)
            return text
        except gdb.error as error:
            return f"<IdString index={index}: {error}>"


class HashlibPrinter(gdb.ValuePrinter):
    def __init__(self, value):
        self._value = value
        value_type = value.type.strip_typedefs()
        self._kind = value_type.tag.split("<", 1)[0].rsplit("::", 1)[-1]
        self._offset = int(value_type.template_argument(1)) if self._kind == "idict" else 0
        self._call_elements = True
        self._item_index = None
        self._item_value = None
        self._error = None

        # Counts must be cheap: DAP requests them even for collapsed values.
        # idict wraps a pool, and mfp wraps an idict.
        try:
            storage = value
            if self._kind == "mfp":
                storage = storage["database"]
            if self._kind in ("idict", "mfp"):
                storage = storage["database"]
            impl = storage["entries"]["_M_impl"]
            self._start = impl["_M_start"]
            start = int(self._start)
            finish = int(impl["_M_finish"])
            end = int(impl["_M_end_of_storage"])
            stride = self._start.type.strip_typedefs().target().sizeof
            if (not start and end) or not start <= finish <= end:
                raise gdb.error("invalid or uninitialized entries")
            if (finish - start) % stride or (end - start) % stride:
                raise gdb.error("invalid entries alignment")
            self._size = (finish - start) // stride
        except gdb.error as error:
            self._error = str(error)
            self._size = 0

    def display_hint(self):
        return "map" if self._kind in ("dict", "idict") else "array"

    def to_string(self):
        if self._error is not None:
            return f"<hashlib::{self._kind}: {self._error}>"
        return f"hashlib::{self._kind} with {self._size} elements"

    def num_children(self):
        return self._size * (2 if self.display_hint() == "map" else 1)

    def _element(self, n):
        if self._item_index == n:
            return self._item_value
        item = None
        if self._call_elements:
            try:
                index = n + self._offset
                item = call_method(self._value, f"element({index}).operator*()")
                item = item.referenced_value()
            except gdb.error:
                # Unused template accessors may have no callable definition,
                # even with -fno-inline. Fall back once per container.
                self._call_elements = False
        if item is None:
            index = self._size - 1 - n if self._kind in ("dict", "pool") else n
            item = (self._start + index).dereference()["udata"]
        self._item_index = n
        self._item_value = item
        return item

    def child(self, n):
        if n < 0 or n >= self.num_children():
            raise IndexError(n)
        try:
            if self._kind == "dict":
                item = self._element(n // 2)
                value = item["second" if n % 2 else "first"]
            elif self._kind == "idict":
                value = self._element(n // 2) if n % 2 else gdb.Value(n // 2 + self._offset)
            else:
                value = self._element(n)
        except gdb.error as error:
            value = f"<{error}>"
        return (f"[{n}]", value)

    def children(self):
        # CLI uses children(); DAP uses num_children() and child() for paging.
        for n in range(self.num_children()):
            yield self.child(n)


class HashlibDAPPrinter(HashlibPrinter):
    # DAP ignores the map hint. Give it one named child per entry instead.
    def display_hint(self):
        return None if self._kind in ("dict", "idict") else "array"

    def num_children(self):
        return self._size

    def child(self, n):
        if n < 0 or n >= self.num_children():
            raise IndexError(n)
        if self._kind not in ("dict", "idict"):
            return super().child(n)
        try:
            item = self._element(n)
            if self._kind == "dict":
                key = item["first"].format_string()
                value = item["second"]
            else:
                key = str(n + self._offset)
                value = item
            return (f"[{key}]", value)
        except gdb.error as error:
            return (f"[{n}]", f"<{error}>")


def hashlib_printer(value):
    printer = HashlibDAPPrinter if "gdb.dap.varref" in sys.modules else HashlibPrinter
    return printer(value)


printers = gdb.printing.RegexpCollectionPrettyPrinter("yosys")
printers.add_printer("vector", r"^std::(?:__\d+::)?vector<.*>$", VectorPrinter)
printers.add_printer(
    "IdString", r"^Yosys::RTLIL::(?:Owning)?IdString$", IdStringPrinter
)
printers.add_printer(
    "hashlib", r"^(?:Yosys::)?hashlib::(?:dict|pool|idict|mfp)<.*>$", hashlib_printer
)
gdb.printing.register_pretty_printer(gdb.current_progspace(), printers, replace=True)
import gdb
import gdb.printing
import sys
from collections import OrderedDict

# /usr/share/gcc/python/libstdcxx/v6/printers.py
sys.path.insert(0, '/usr/share/gcc/python')
from libstdcxx.v6.printers import register_libstdcxx_printers
register_libstdcxx_printers (None)


class VectorPrinter(gdb.ValuePrinter):
    def __init__(self, value):
        self._error = None
        self._size = self._capacity = 0
        self._is_bool = value.type.strip_typedefs().template_argument(0).code == gdb.TYPE_CODE_BOOL
        try:
            impl = value["_M_impl"]
            self._start = impl["_M_start"]
            finish = impl["_M_finish"]
            end = int(impl["_M_end_of_storage"])
            self._bit_offset = 0
            if self._is_bool:
                self._bit_offset = int(self._start["_M_offset"])
                finish_offset = int(finish["_M_offset"])
                self._start = self._start["_M_p"]
                finish = finish["_M_p"]
            start, finish = int(self._start), int(finish)
            stride = self._start.type.strip_typedefs().target().sizeof
            if (not start and end) or not start <= finish <= end:
                raise gdb.error("invalid or uninitialized storage")
            if (finish - start) % stride or (end - start) % stride:
                raise gdb.error("invalid storage alignment")
            self._size = (finish - start) // stride
            self._capacity = (end - start) // stride
            if self._is_bool:
                self._word_bits = 8 * stride
                if not (0 <= self._bit_offset < self._word_bits and
                        0 <= finish_offset < self._word_bits):
                    raise gdb.error("invalid bit offsets")
                self._size = self._size * self._word_bits + finish_offset - self._bit_offset
                self._capacity = self._capacity * self._word_bits - self._bit_offset
                if not 0 <= self._size <= self._capacity:
                    raise gdb.error("invalid or uninitialized storage")
        except gdb.error as error:
            self._error = str(error)
            self._size = 0

    def display_hint(self):
        return "array"

    def to_string(self):
        if self._error is not None:
            return f"<std::vector: {self._error}>"
        name = "std::vector<bool>" if self._is_bool else "std::vector"
        return f"{name} of length {self._size}, capacity {self._capacity}"

    def num_children(self):
        # DAP otherwise materializes children() just to count a collapsed vector.
        return self._size

    def child(self, n):
        if n < 0 or n >= self._size:
            raise IndexError(n)
        if self._is_bool:
            word, bit = divmod(n + self._bit_offset, self._word_bits)
            value = bool((self._start + word).dereference() & (1 << bit))
        else:
            value = (self._start + n).dereference()
        return (f"[{n}]", value)

    def children(self):
        for n in range(self._size):
            yield self.child(n)


_calling = False
_id_cache = OrderedDict()


if "clear_id_cache" in globals():
    for event in (gdb.events.cont, gdb.events.exited, gdb.events.new_objfile):
        event.disconnect(clear_id_cache)


def clear_id_cache(event):
    if not _calling:
        _id_cache.clear()


for event in (gdb.events.cont, gdb.events.exited, gdb.events.new_objfile):
    event.connect(clear_id_cache)


def call_method(value, method):
    global _calling
    if _calling or value.address is None:
        raise gdb.error("inferior call unavailable")

    # GDB's DAP adapter emits continued/stopped for inferior calls. Zed
    # refreshes variables on stopped, which otherwise calls us forever.
    dap_events = sys.modules.get("gdb.dap.events")
    dap_handler = getattr(dap_events, "_on_inferior_call", None)
    if dap_handler is not None:
        gdb.events.inferior_call.disconnect(dap_handler)

    try:
        _calling = True
        address = int(value.address)
        value_type = value.type.strip_typedefs().unqualified()
        return gdb.parse_and_eval(
            f"((const '{value_type}' *)0x{address:x})->{method}"
        )
    finally:
        _calling = False
        if dap_handler is not None:
            gdb.events.inferior_call.connect(dap_handler)


class IdStringPrinter:
    def __init__(self, value):
        self.value = value

    def display_hint(self):
        return "string"

    def to_string(self):
        index = int(self.value["index_"])
        key = (gdb.selected_inferior().num, index)
        if key in _id_cache:
            _id_cache.move_to_end(key)
            return _id_cache[key]
        if _calling or self.value.address is None:
            return f"<IdString index={index}>"

        try:
            result = call_method(self.value, "c_str()")
            text = result.string(errors="replace")
            # Bound retained strings without limiting the displayed value.
            if len(text) <= 4096:
                _id_cache[key] = text
                if len(_id_cache) > 4096:
                    _id_cache.popitem(last=False)
            return text
        except gdb.error as error:
            return f"<IdString index={index}: {error}>"


class HashlibPrinter(gdb.ValuePrinter):
    def __init__(self, value):
        self._value = value
        value_type = value.type.strip_typedefs()
        self._kind = value_type.tag.split("<", 1)[0].rsplit("::", 1)[-1]
        self._offset = int(value_type.template_argument(1)) if self._kind == "idict" else 0
        self._call_elements = True
        self._item_index = None
        self._item_value = None
        self._error = None

        # Counts must be cheap: DAP requests them even for collapsed values.
        # idict wraps a pool, and mfp wraps an idict.
        try:
            storage = value
            if self._kind == "mfp":
                storage = storage["database"]
            if self._kind in ("idict", "mfp"):
                storage = storage["database"]
            impl = storage["entries"]["_M_impl"]
            self._start = impl["_M_start"]
            start = int(self._start)
            finish = int(impl["_M_finish"])
            end = int(impl["_M_end_of_storage"])
            stride = self._start.type.strip_typedefs().target().sizeof
            if (not start and end) or not start <= finish <= end:
                raise gdb.error("invalid or uninitialized entries")
            if (finish - start) % stride or (end - start) % stride:
                raise gdb.error("invalid entries alignment")
            self._size = (finish - start) // stride
        except gdb.error as error:
            self._error = str(error)
            self._size = 0

    def display_hint(self):
        return "map" if self._kind in ("dict", "idict") else "array"

    def to_string(self):
        if self._error is not None:
            return f"<hashlib::{self._kind}: {self._error}>"
        return f"hashlib::{self._kind} with {self._size} elements"

    def num_children(self):
        return self._size * (2 if self.display_hint() == "map" else 1)

    def _element(self, n):
        if self._item_index == n:
            return self._item_value
        item = None
        if self._call_elements:
            try:
                index = n + self._offset
                item = call_method(self._value, f"element({index}).operator*()")
                item = item.referenced_value()
            except gdb.error:
                # Unused template accessors may have no callable definition,
                # even with -fno-inline. Fall back once per container.
                self._call_elements = False
        if item is None:
            index = self._size - 1 - n if self._kind in ("dict", "pool") else n
            item = (self._start + index).dereference()["udata"]
        self._item_index = n
        self._item_value = item
        return item

    def child(self, n):
        if n < 0 or n >= self.num_children():
            raise IndexError(n)
        try:
            if self._kind == "dict":
                item = self._element(n // 2)
                value = item["second" if n % 2 else "first"]
            elif self._kind == "idict":
                value = self._element(n // 2) if n % 2 else gdb.Value(n // 2 + self._offset)
            else:
                value = self._element(n)
        except gdb.error as error:
            value = f"<{error}>"
        return (f"[{n}]", value)

    def children(self):
        # CLI uses children(); DAP uses num_children() and child() for paging.
        for n in range(self.num_children()):
            yield self.child(n)


class HashlibDAPPrinter(HashlibPrinter):
    # DAP ignores the map hint. Give it one named child per entry instead.
    def display_hint(self):
        return None if self._kind in ("dict", "idict") else "array"

    def num_children(self):
        return self._size

    def child(self, n):
        if n < 0 or n >= self.num_children():
            raise IndexError(n)
        if self._kind not in ("dict", "idict"):
            return super().child(n)
        try:
            item = self._element(n)
            if self._kind == "dict":
                key = item["first"].format_string()
                value = item["second"]
            else:
                key = str(n + self._offset)
                value = item
            return (f"[{key}]", value)
        except gdb.error as error:
            return (f"[{n}]", f"<{error}>")


def hashlib_printer(value):
    printer = HashlibDAPPrinter if "gdb.dap.varref" in sys.modules else HashlibPrinter
    return printer(value)


printers = gdb.printing.RegexpCollectionPrettyPrinter("yosys")
printers.add_printer("vector", r"^std::(?:__\d+::)?vector<.*>$", VectorPrinter)
printers.add_printer(
    "IdString", r"^Yosys::RTLIL::(?:Owning)?IdString$", IdStringPrinter
)
printers.add_printer(
    "hashlib", r"^(?:Yosys::)?hashlib::(?:dict|pool|idict|mfp)<.*>$", hashlib_printer
)
gdb.printing.register_pretty_printer(gdb.current_progspace(), printers, replace=True)

import gdb
import gdb.printing
import sys
from collections import OrderedDict

# /usr/share/gcc/python/libstdcxx/v6/printers.py
sys.path.insert(0, '/usr/share/gcc/python')
from libstdcxx.v6.printers import register_libstdcxx_printers, unique_ptr_get
if not any(getattr(printer, "name", None) == "libstdc++-v6" for printer in gdb.pretty_printers):
    register_libstdcxx_printers(None)


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


class SpanPrinter(gdb.ValuePrinter):
    def __init__(self, value):
        self._error = None
        self._size = 0
        try:
            value_type = value.type.strip_typedefs()
            self._start = value["_M_ptr"]
            extent = value_type.template_argument(1)
            dynamic_extent = (1 << (extent.type.sizeof * 8)) - 1
            self._size = (int(value["_M_extent"]["_M_extent_value"])
                          if int(extent) == dynamic_extent else int(extent))
            if self._size < 0 or (self._size and not int(self._start)):
                raise gdb.error("invalid or uninitialized storage")
        except (gdb.error, ValueError) as error:
            self._error = str(error)
            self._size = 0

        # DAP allocates a child cache for the entire reported size, even when
        # requesting one page. Uninitialized spans can report enormous sizes.
        self._shown = min(self._size, 256) if "gdb.dap.varref" in sys.modules else self._size

    def display_hint(self):
        return "array"

    def to_string(self):
        if self._error is not None:
            return f"<std::span: {self._error}>"
        summary = f"std::span of length {self._size}"
        if self._shown < self._size:
            summary += f" (showing first {self._shown})"
        return summary

    def num_children(self):
        return self._shown

    def child(self, n):
        if n < 0 or n >= self._shown:
            raise IndexError(n)
        return (f"[{n}]", (self._start + n).dereference())

    def children(self):
        for n in range(self._shown):
            yield self.child(n)


class ConstPrinter(gdb.ValuePrinter):
    def __init__(self, value):
        self._error = None
        self._size = 0
        self._unsigned = None
        self._preview = ""
        try:
            if value.type.strip_typedefs().tag == "ir::Const":
                value = value["raw_"]
            self._state_type = value["bits_"].type.template_argument(0)
            tag = int(value["tag"])
            if tag == 0:
                self._packed = False
                self._bits = VectorPrinter(value["bits_"])
                if self._bits._error is not None:
                    raise gdb.error(self._bits._error)
                self._size = self._bits.num_children()
                self._start = self._bits._start
            elif tag == 1:
                self._packed = True
                storage = value["str_"]
                self._start = storage["_M_dataplus"]["_M_p"]
                self._size = int(storage["_M_string_length"]) * 8
                if self._size and not int(self._start):
                    raise gdb.error("invalid or uninitialized string storage")
            else:
                raise gdb.error("invalid constant representation")

            if not 0 <= self._size < (1 << 30):
                raise gdb.error("invalid or uninitialized constant width")
            if not self._size:
                self._unsigned = 0
            elif self._packed:
                # String backing stores packed bytes in most-significant order.
                count = self._size // 8
                data = bytes(gdb.selected_inferior().read_memory(self._start, min(count, 512)))
                if count <= 512:
                    self._unsigned = int.from_bytes(data, "big")
                self._preview = "".join(f"{byte:08b}" for byte in data[:8])
            else:
                # Keep summaries bounded, including for uninitialized locals.
                count = min(self._size, 4096)
                data = bytes(gdb.selected_inferior().read_memory(
                    self._start + self._size - count, count
                ))
                if any(bit > 5 for bit in data):
                    raise gdb.error("invalid constant bit state")
                if count == self._size and all(bit < 2 for bit in data):
                    self._unsigned = 0
                    for bit in reversed(data):
                        self._unsigned = (self._unsigned << 1) | bit
                self._preview = "".join("01xz-m"[bit] for bit in reversed(data[-64:]))
        except (gdb.error, ValueError) as error:
            self._error = str(error)

        self._shown = 0 if self._error or self._unsigned is not None else self._size
        if "gdb.dap.varref" in sys.modules:
            self._shown = min(self._shown, 256)

    def display_hint(self):
        return "array" if self._unsigned is None else None

    def to_string(self):
        if self._error is not None:
            return f"<RTLIL::Const: {self._error}>"
        if self._unsigned is not None:
            return str(self._unsigned)
        suffix = "..." if self._size > 64 else ""
        return f"{self._size}'b{self._preview}{suffix}"

    def num_children(self):
        return self._shown

    def child(self, n):
        if n < 0 or n >= self._shown:
            raise IndexError(n)
        if self._packed:
            byte = int((self._start + self._size // 8 - 1 - n // 8).dereference()) & 0xff
            value = gdb.Value((byte >> (n % 8)) & 1).cast(self._state_type)
        else:
            value = self._bits.child(n)[1]
        return (f"[{n}]", value)

    def children(self):
        for n in range(self._shown):
            yield self.child(n)


class AstNodePrinter(gdb.ValuePrinter):
    def __init__(self, value):
        self._value = None
        self._error = None
        self._fields = []
        try:
            value_type = value.type.strip_typedefs()
            if value_type.code == gdb.TYPE_CODE_REF:
                value = value.referenced_value()
                value_type = value.type.strip_typedefs()
            if str(value_type).startswith("std::"):
                value = unique_ptr_get(value)
            if value.type.code == gdb.TYPE_CODE_PTR:
                if int(value) == 0:
                    return
                value = value.dereference()
            # Put the useful AST information first without hiding other fields.
            fields = [field.name for field in value.type.fields() if field.name]
            first = ("type", "location", "str", "children", "bits", "attributes", "id2ast")
            self._fields = [name for name in first if name in fields]
            self._fields.extend(name for name in fields if name not in first)
            self._value = value
        except (gdb.error, ValueError) as error:
            self._error = str(error)

    @staticmethod
    def _string(value):
        text = gdb.default_visualizer(value).to_string()
        if isinstance(text, gdb.LazyString):
            length = min(text.length, 200)
            result = text.value().string(length=length, errors="replace")
            return result + ("..." if text.length > length else "")
        return str(text)

    def to_string(self):
        if self._error is not None:
            return f"<AstNode: {self._error}>"
        if self._value is None:
            return "nullptr"
        try:
            kind = str(self._value["type"]).rsplit("::", 1)[-1]
            parts = [kind]
            name = self._string(self._value["str"])
            if name:
                parts.append(repr(name))
            if kind == "AST_CONSTANT":
                bits = VectorPrinter(self._value["bits"])
                if bits._error is not None:
                    raise gdb.error(bits._error)
                size = bits.num_children()
                digits = "".join(
                    "01xz-m"[int(bits.child(i)[1])]
                    for i in range(size - 1, max(-1, size - 65), -1)
                )
                parts.append(f"{size}'b{digits}" + ("..." if size > 64 else ""))
            elif kind == "AST_REALVALUE":
                parts.append(str(self._value["realvalue"]))
            begin = self._value["location"]["begin"]
            filename = begin["filename"]["_M_ptr"]
            source = self._string(filename.dereference()) if int(filename) else "?"
            parts.append(f"<{source}:{int(begin['line'])}:{int(begin['column'])}>")
            return " ".join(parts)
        except (gdb.error, ValueError, IndexError) as error:
            return f"<AstNode: {error}>"

    def num_children(self):
        return len(self._fields)

    def child(self, n):
        if n < 0 or n >= self.num_children():
            raise IndexError(n)
        name = self._fields[n]
        return (name, self._value[name])

    def children(self):
        for n in range(self.num_children()):
            yield self.child(n)


_id_cache = OrderedDict()


if "clear_id_cache" in globals():
    for event in (gdb.events.cont, gdb.events.exited, gdb.events.new_objfile):
        event.disconnect(clear_id_cache)


def clear_id_cache(event):
    _id_cache.clear()


for event in (gdb.events.cont, gdb.events.exited, gdb.events.new_objfile):
    event.connect(clear_id_cache)


def deque_element(value, index):
    impl = value["_M_impl"]
    start, finish = impl["_M_start"], impl["_M_finish"]
    capacity = int(start["_M_last"] - start["_M_first"])
    size = int(finish["_M_node"] - start["_M_node"]) * capacity
    size += int(finish["_M_cur"] - finish["_M_first"])
    size -= int(start["_M_cur"] - start["_M_first"])
    if capacity <= 0 or not 0 <= index < size:
        raise gdb.error("invalid deque index")
    offset = int(start["_M_cur"] - start["_M_first"]) + index
    block = (start["_M_node"] + offset // capacity).dereference()
    return (block + offset % capacity).dereference()


def id_name(value, pool=None):
    raw = int(value["value"])
    width = value["value"].type.sizeof * 8
    if raw == (1 << width) - 1:
        return ""
    public = bool(raw & (1 << (width - 1)))
    index = raw & ((1 << (32 if width == 64 else 31)) - 1)
    pool_address = int(pool.address) if pool is not None else 0
    key = (gdb.selected_inferior().num, pool_address, raw)
    if key in _id_cache:
        return _id_cache[key]
    static_count = int(gdb.parse_and_eval("Yosys::STATIC_TWINE_END"))
    fragments, seen = [], set()
    while index not in seen:
        seen.add(index)
        if len(seen) > 256:
            raise gdb.error("twine prefix chain too deep")
        if index < static_count:
            nodes = VectorPrinter(gdb.parse_and_eval("Yosys::StaticTwines::nodes_"))
            node = nodes.child(index)[1]
        elif pool is not None:
            node = deque_element(pool["backing"], index - static_count)
        else:
            return f"<IdString index={index}>"
        text = node["text_"]
        length = int(text["len_"])
        if length > 4096:
            raise gdb.error("twine text too long")
        data = text["inl_"] if length <= 8 else text["ptr_"]
        fragments.append(data.string(length=length, errors="replace"))
        index = int(node["prefix_"])
        if index == 0xffffffff:
            result = ("\\" if public else "") + "".join(reversed(fragments))
            if len(_id_cache) >= 4096:
                _id_cache.popitem(last=False)
            _id_cache[key] = result
            return result
        if index == 0xfffffffe:
            raise gdb.error("dead twine")
    raise gdb.error("cyclic twine prefix")


def wire_name(wire):
    pool = wire["module"]["design"]["twines_"]
    return id_name(wire["name"]["id_"], pool)


class IdStringPrinter:
    def __init__(self, value):
        self.value = value

    def display_hint(self):
        return "string"

    def to_string(self):
        try:
            value_type = self.value.type.strip_typedefs()
            if value_type.tag == "Yosys::IdString":
                return id_name(self.value)
            if value_type.tag == "Yosys::RTLIL::PooledName":
                pool = self.value["pool_"]
                return id_name(self.value["id_"], pool.dereference() if int(pool) else None)
            owner_type = value_type.template_argument(0)
            slot = str(value_type.template_argument(1))
            field_name = "type" if slot.endswith("CellTypeSlot") else "name"
            offset = next(field.bitpos // 8 for field in owner_type.fields() if field.name == field_name)
            address = self.value.address.cast(gdb.lookup_type("char").pointer()) - offset
            owner = address.cast(owner_type.pointer()).dereference()
            design = owner["design"] if owner_type.tag == "Yosys::RTLIL::Module" else owner["module"]["design"]
            return id_name(self.value["id_"], design["twines_"])
        except (gdb.error, StopIteration, ValueError) as error:
            return f"<IdString: {error}>"


def wire_slice(wire, high, low):
    # Use RTLIL offsets, matching SigBit::offset rather than HDL declaration indices.
    name = wire_name(wire)
    return f"{name}[{low}]" if high == low else f"{name}[{high}:{low}]"


class SigBitPrinter(gdb.ValuePrinter):
    def __init__(self, value):
        self._value = value

    def to_string(self):
        try:
            if int(self._value["wire"]):
                offset = int(self._value["offset"])
                return wire_slice(self._value["wire"], offset, offset)
            return "1'b" + "01xz-m"[int(self._value["data"])]
        except (gdb.error, IndexError) as error:
            return f"<SigBit: {error}>"

    def children(self):
        if int(self._value["wire"]):
            yield ("wire", self._value["wire"])
            yield ("offset", self._value["offset"])
        else:
            yield ("data", self._value["data"])


class SigChunkPrinter(gdb.ValuePrinter):
    def __init__(self, value):
        self._value = value

    def to_string(self):
        try:
            width = int(self._value["width"])
            if width < 0:
                raise gdb.error("negative width")
            if not width:
                return "{}"
            if int(self._value["wire"]):
                low = int(self._value["offset"])
                return wire_slice(self._value["wire"], low + width - 1, low)
            data = VectorPrinter(self._value["data"])
            digits = "".join(
                "01xz-m"[int(data.child(i)[1])]
                for i in range(width - 1, max(-1, width - 65), -1)
            )
            return f"{width}'b{digits}" + ("..." if width > 64 else "")
        except (gdb.error, IndexError) as error:
            return f"<SigChunk: {error}>"

    def children(self):
        fields = ("wire", "offset", "width") if int(self._value["wire"]) else ("data", "width")
        for name in fields:
            yield (name, self._value[name])


class SigSpecPrinter(gdb.ValuePrinter):
    def __init__(self, value):
        self._value = value
        self._error = None
        self._chunk = None
        self._bits = None
        self._size = 0
        try:
            rep = int(value["rep_"])
            if rep == 0:
                self._chunk = value["chunk_"]
                self._size = int(self._chunk["width"])
                if self._size < 0:
                    raise gdb.error("negative width")
            elif rep == 1:
                self._bits = VectorPrinter(value["bits_"])
                if self._bits._error is not None:
                    raise gdb.error(self._bits._error)
                self._size = self._bits.num_children()
            else:
                raise gdb.error("invalid signal representation")
        except gdb.error as error:
            self._error = str(error)

    def to_string(self):
        try:
            return self._summary()
        except (gdb.error, IndexError) as error:
            return f"<SigSpec: {error}>"

    def _summary(self):
        if self._error is not None:
            return f"<SigSpec: {self._error}>"
        if not self._size:
            return "{} (0 bits)"
        if self._chunk is not None:
            text = SigChunkPrinter(self._chunk).to_string()
        else:
            # Summaries are bounded; all bits remain available on expansion.
            runs = []
            for i in range(self._size - 1, max(-1, self._size - 65), -1):
                bit = self._bits.child(i)[1]
                wire = int(bit["wire"])
                if wire:
                    offset = int(bit["offset"])
                    if runs and runs[-1][0] == wire and runs[-1][3] == offset + 1:
                        runs[-1][3] = offset
                    else:
                        runs.append([wire, bit["wire"], offset, offset])
                else:
                    digit = "01xz-m"[int(bit["data"])]
                    if runs and runs[-1][0] == 0:
                        runs[-1][1] += digit
                    else:
                        runs.append([0, digit])
            parts = [
                wire_slice(run[1], run[2], run[3]) if run[0]
                else f"{len(run[1])}'b{run[1]}"
                for run in runs
            ]
            if self._size > 64:
                parts.append("...")
            text = parts[0] if len(parts) == 1 else "{ " + ", ".join(parts) + " }"
        unit = "bit" if self._size == 1 else "bits"
        return f"{text} ({self._size} {unit})"

    def num_children(self):
        return 0 if self._error else (1 if self._chunk is not None and self._size else self._size)

    def child(self, n):
        if n < 0 or n >= self.num_children():
            raise IndexError(n)
        return ("chunk", self._chunk) if self._chunk is not None else self._bits.child(n)

    def children(self):
        for n in range(self.num_children()):
            yield self.child(n)


class SigSigPrinter(gdb.ValuePrinter):
    def __init__(self, value):
        self._value = value

    def to_string(self):
        return f"{SigSpecPrinter(self._value['first']).to_string()} := {SigSpecPrinter(self._value['second']).to_string()}"

    def children(self):
        yield ("lhs", self._value["first"])
        yield ("rhs", self._value["second"])


class HashlibPrinter(gdb.ValuePrinter):
    def __init__(self, value):
        self._value = value
        value_type = value.type.strip_typedefs()
        self._kind = value_type.tag.split("<", 1)[0].rsplit("::", 1)[-1]
        self._offset = int(value_type.template_argument(1)) if self._kind == "idict" else 0
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
        item_type = self._value.type.strip_typedefs().template_argument(0).strip_typedefs()
        if self._kind == "pool" and item_type.tag == "Yosys::RTLIL::SigBit":
            bits = [SigBitPrinter(self._element(i)).to_string() for i in range(min(self._size, 8))]
            if self._size > 8:
                bits.append("...")
            unit = "bit" if self._size == 1 else "bits"
            return "{ " + ", ".join(bits) + f" }} ({self._size} {unit})"
        return f"hashlib::{self._kind} with {self._size} elements"

    def num_children(self):
        return self._size * (2 if self.display_hint() == "map" else 1)

    def _element(self, n):
        if self._item_index == n:
            return self._item_value
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
                key = item["first"].format_string(max_depth=0)
                printer = gdb.default_visualizer(item["first"])
                if printer is not None:
                    summary = printer.to_string()
                    if isinstance(summary, str):
                        key = summary
                value = item["second"]
            else:
                key = str(n + self._offset)
                value = item
            return (f"[{key}]", value)
        except gdb.error as error:
            return (f"[{n}]", f"<{error}>")


class StackMapPrinter(gdb.ValuePrinter):
    def __init__(self, value):
        self._current = HashlibDAPPrinter(value["current_state"])
        self._saved = value["backup_state"]

    def to_string(self):
        depth = VectorPrinter(self._saved).num_children()
        return f"{self._current._size} mappings, {depth} saved scopes"

    def num_children(self):
        return self._current.num_children() + 1

    def child(self, n):
        if n < 0 or n >= self.num_children():
            raise IndexError(n)
        if n == self._current.num_children():
            return ("saved_scopes", self._saved)
        return self._current.child(n)

    def children(self):
        for n in range(self.num_children()):
            yield self.child(n)


def hashlib_printer(value):
    printer = HashlibDAPPrinter if "gdb.dap.varref" in sys.modules else HashlibPrinter
    return printer(value)


def ast_node_pointer_printer(value):
    # Pointer types have no tag/name for RegexpCollectionPrettyPrinter to match.
    value_type = value.type.strip_typedefs()
    if value_type.code == gdb.TYPE_CODE_PTR:
        target = value_type.target().strip_typedefs().unqualified()
        if target.tag == "Yosys::AST::AstNode":
            return AstNodePrinter(value)


printers = gdb.printing.RegexpCollectionPrettyPrinter("yosys")
printers.add_printer("vector", r"^std::(?:__\d+::)?vector<.*>$", VectorPrinter)
printers.add_printer("span", r"^std::(?:__\d+::)?span<.*>$", SpanPrinter)
printers.add_printer("Const", r"^(?:Yosys::RTLIL|ir)::Const$", ConstPrinter)
printers.add_printer("AstNode", r"^Yosys::AST::AstNode$", AstNodePrinter)
printers.add_printer(
    "AstNodePtr", r"^std::(?:__\d+::)?unique_ptr<Yosys::AST::AstNode(?:,.*)?>$", AstNodePrinter
)
printers.add_printer(
    "IdString", r"^Yosys::(?:IdString|RTLIL::PooledName|RTLIL::OwnedId<.*>)$", IdStringPrinter
)
printers.add_printer("SigBit", r"^Yosys::RTLIL::SigBit$", SigBitPrinter)
printers.add_printer("SigChunk", r"^Yosys::RTLIL::SigChunk$", SigChunkPrinter)
printers.add_printer("SigSpec", r"^Yosys::RTLIL::SigSpec$", SigSpecPrinter)
printers.add_printer(
    "SigSig", r"^std::pair<Yosys::RTLIL::SigSpec, Yosys::RTLIL::SigSpec>$", SigSigPrinter
)
printers.add_printer("stackmap", r"^Yosys::stackmap<.*>$", StackMapPrinter)
printers.add_printer(
    "hashlib", r"^(?:Yosys::)?hashlib::(?:dict|pool|idict|mfp)<.*>$", hashlib_printer
)
gdb.printing.register_pretty_printer(gdb.current_progspace(), printers, replace=True)
gdb.printing.register_pretty_printer(gdb.current_progspace(), ast_node_pointer_printer, replace=True)

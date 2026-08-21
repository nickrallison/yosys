python
import gdb
import gdb.printing
import glob
import os
import sys


_MAX_CHILDREN = 64
_MAX_BITS = 256
_STATE_CHARS = {0: "0", 1: "1", 2: "x", 3: "z", 4: "-", 5: "m"}
_SYNC_TYPES = {
    0: "low", 1: "high", 2: "posedge", 3: "negedge",
    4: "edge", 5: "always", 6: "global", 7: "init",
}


def _register_libstdcxx_printers():
    if getattr(gdb, "_yosys_libstdcxx_printers", False):
        return
    try:
        import libstdcxx.v6.printers
    except ImportError:
        for directory in glob.glob("/usr/share/gcc*/python") + glob.glob("/usr/local/share/gcc*/python"):
            if os.path.isdir(os.path.join(directory, "libstdcxx")):
                sys.path.insert(0, directory)
                try:
                    import libstdcxx.v6.printers
                    break
                except ImportError:
                    continue
        else:
            return
    libstdcxx.v6.printers.register_libstdcxx_printers(None)
    gdb._yosys_libstdcxx_printers = True


_register_libstdcxx_printers()


def _integer(value):
    try:
        return int(value)
    except (gdb.error, TypeError, ValueError):
        return 0


def _pointer(value):
    return _integer(value) != 0


def _vector_size(value):
    impl = value["_M_impl"]
    return _integer(impl["_M_finish"] - impl["_M_start"])


def _vector_at(value, index):
    return (value["_M_impl"]["_M_start"] + index).dereference()


def _vector_values(value, limit=_MAX_CHILDREN):
    size = _vector_size(value)
    for index in range(min(size, limit)):
        yield _vector_at(value, index)


def _string(value):
    try:
        pointer = value["_M_dataplus"]["_M_p"]
        length = _integer(value["_M_string_length"])
        return pointer.string(encoding="utf-8", errors="replace", length=length)
    except (gdb.error, gdb.MemoryError):
        return str(value)


def _string_bytes(value):
    pointer = value["_M_dataplus"]["_M_p"]
    length = _integer(value["_M_string_length"])
    return bytes(gdb.selected_inferior().read_memory(_integer(pointer), length))


def _state(value):
    return _STATE_CHARS.get(_integer(value), "?")


def _id(value):
    index = _integer(value["index_"])
    if index < 0:
        return "<autoidx {}>".format(-index)
    try:
        storage = gdb.parse_and_eval("Yosys::RTLIL::IdString::global_id_storage_")
        entry = _vector_at(storage, index)
        return entry["buf"].string(
            encoding="utf-8", errors="replace", length=_integer(entry["size"])
        )
    except (gdb.error, RuntimeError, ValueError):
        return "<IdString {}>".format(index)


def _dict_size(value):
    return _vector_size(value["entries"])


def _flags(value):
    flags = _integer(value["flags"])
    result = []
    if flags & 1:
        result.append("string")
    if flags & 2:
        result.append("signed")
    if flags & 4:
        result.append("real")
    if flags & 8:
        result.append("unsized")
    return " " + ", ".join(result) if result else ""


def _constant_bits(value):
    return list(_vector_values(value["bits_"], _MAX_BITS + 1))


def _constant(value):
    if _integer(value["tag"]) != 0:
        data = _string_bytes(value["str_"])
        if _integer(value["flags"]) & 1:
            return "string {!r}".format(data.decode("utf-8", errors="backslashreplace"))
        width = len(data) * 8
        if width > _MAX_BITS:
            return "Const<{}>".format(width)
        return "{}'b{}".format(width, "".join("{:08b}".format(byte) for byte in data))
    bits = _constant_bits(value)
    width = _vector_size(value["bits_"])
    if width > _MAX_BITS:
        return "Const<{}>".format(width)
    return "{}'b{}".format(width, "".join(_state(bit) for bit in reversed(bits)))


def _wire_bit(value):
    wire = value["wire"]
    if not _pointer(wire):
        return _state(value["data"])
    try:
        return "{}[{}]".format(_id(wire.dereference()["name"]), _integer(value["offset"]))
    except gdb.error:
        return "<wire@{}>[{}]".format(wire, _integer(value["offset"]))


def _chunk_bits(value):
    width = _integer(value["width"])
    wire = value["wire"]
    if _pointer(wire):
        return [(wire, _integer(value["offset"]) + index) for index in range(width)]
    return [(None, _state(bit)) for bit in _vector_values(value["data"], width)]


def _sigspec_bits(value):
    if _integer(value["rep_"]) == 0:
        return _chunk_bits(value["chunk_"])
    bits = []
    for bit in _vector_values(value["bits_"], _MAX_BITS + 1):
        wire = bit["wire"]
        bits.append((wire, _integer(bit["offset"]) if _pointer(wire) else _state(bit["data"])))
    return bits


def _signal(value):
    width = _integer(value["chunk_"]["width"]) if _integer(value["rep_"]) == 0 else _vector_size(value["bits_"])
    if width > _MAX_BITS:
        return "SigSpec<{}>".format(width)
    bits = _sigspec_bits(value)
    if not bits:
        return "{}'b".format(width)
    parts = []
    index = len(bits) - 1
    while index >= 0:
        wire, data = bits[index]
        if not _pointer(wire):
            states = []
            while index >= 0 and not _pointer(bits[index][0]):
                states.append(bits[index][1])
                index -= 1
            parts.append("{}'b{}".format(len(states), "".join(states)))
            continue
        high = data
        low = data
        index -= 1
        while index >= 0 and _pointer(bits[index][0]) and _integer(bits[index][0]) == _integer(wire) and bits[index][1] == low - 1:
            low = bits[index][1]
            index -= 1
        try:
            name = _id(wire.dereference()["name"])
        except gdb.error:
            name = "<wire@{}>".format(wire)
        parts.append("{}[{}]".format(name, high) if high == low else "{}[{}:{}]".format(name, high, low))
    return parts[0] if len(parts) == 1 else "{{{}}}".format(", ".join(parts))


class IdStringPrinter:
    def __init__(self, value):
        self.value = value

    def to_string(self):
        return _id(self.value)


class ConstPrinter:
    def __init__(self, value):
        self.value = value

    def to_string(self):
        return _constant(self.value) + _flags(self.value)


class SigBitPrinter:
    def __init__(self, value):
        self.value = value

    def to_string(self):
        return _wire_bit(self.value)


class SigChunkPrinter:
    def __init__(self, value):
        self.value = value

    def to_string(self):
        wire = self.value["wire"]
        width = _integer(self.value["width"])
        if not _pointer(wire):
            return "{}'b{}".format(width, "".join(reversed([data for _, data in _chunk_bits(self.value)])))
        try:
            name = _id(wire.dereference()["name"])
        except gdb.error:
            name = "<wire@{}>".format(wire)
        offset = _integer(self.value["offset"])
        return "{}[{}]".format(name, offset) if width == 1 else "{}[{}:{}]".format(name, offset + width - 1, offset)


class SigSpecPrinter:
    def __init__(self, value):
        self.value = value

    def to_string(self):
        return _signal(self.value)


class NamedObjectPrinter:
    def __init__(self, value, kind):
        self.value = value
        self.kind = kind

    def to_string(self):
        name = _id(self.value["name"])
        if self.kind == "Wire":
            width = _integer(self.value["width"])
            offset = _integer(self.value["start_offset"])
            end = offset + width - 1
            direction = []
            if bool(self.value["port_input"]):
                direction.append("input")
            if bool(self.value["port_output"]):
                direction.append("output")
            if bool(self.value["is_signed"]):
                direction.append("signed")
            suffix = " " + " ".join(direction) if direction else ""
            return "Wire {} [{}:{}]{}".format(name, end, offset, suffix)
        if self.kind == "Memory":
            return "Memory {} [{} x {}]".format(name, _integer(self.value["size"]), _integer(self.value["width"]))
        if self.kind == "Cell":
            return "Cell {} ({}, {} ports, {} parameters)".format(name, _id(self.value["type"]), _dict_size(self.value["connections_"]), _dict_size(self.value["parameters"]))
        if self.kind == "Module":
            return "Module {} ({} wires, {} cells, {} memories, {} processes)".format(name, _dict_size(self.value["wires_"]), _dict_size(self.value["cells_"]), _dict_size(self.value["memories"]), _dict_size(self.value["processes"]))
        if self.kind == "Process":
            return "Process {} ({} sync rules)".format(name, _vector_size(self.value["syncs"]))
        return "{} {}".format(self.kind, name)


class DesignPrinter:
    def __init__(self, value):
        self.value = value

    def to_string(self):
        return "Design ({} modules, {} selections)".format(_dict_size(self.value["modules_"]), _vector_size(self.value["selection_stack"]))


class SelectionPrinter:
    def __init__(self, value):
        self.value = value

    def to_string(self):
        if bool(self.value["complete_selection"]):
            return "Selection (complete)"
        if bool(self.value["full_selection"]):
            return "Selection (full)"
        return "Selection ({} modules, {} partial modules)".format(_dict_size(self.value["selected_modules"]), _dict_size(self.value["selected_members"]))


class CaseRulePrinter:
    def __init__(self, value):
        self.value = value

    def to_string(self):
        return "CaseRule ({} compare values, {} actions, {} switches)".format(_vector_size(self.value["compare"]), _vector_size(self.value["actions"]), _vector_size(self.value["switches"]))


class SwitchRulePrinter:
    def __init__(self, value):
        self.value = value

    def to_string(self):
        return "SwitchRule ({}, {} cases)".format(_signal(self.value["signal"]), _vector_size(self.value["cases"]))


class SyncRulePrinter:
    def __init__(self, value):
        self.value = value

    def to_string(self):
        return "SyncRule ({}, {}, {} actions, {} memory writes)".format(_SYNC_TYPES.get(_integer(self.value["type"]), "unknown"), _signal(self.value["signal"]), _vector_size(self.value["actions"]), _vector_size(self.value["mem_write_actions"]))


class MemWriteActionPrinter:
    def __init__(self, value):
        self.value = value

    def to_string(self):
        return "MemWriteAction {} [{}] <- {}".format(_id(self.value["memid"]), _signal(self.value["address"]), _signal(self.value["data"]))


class AstNodePrinter:
    def __init__(self, value):
        self.value = value

    def to_string(self):
        node_type = str(self.value["type"]).rsplit("::", 1)[-1]
        string = _string(self.value["str"])
        children = _vector_size(self.value["children"])
        suffix = " {}".format(string) if string else ""
        return "{}{} ({} children)".format(node_type, suffix, children)

    def children(self):
        yield "type", self.value["type"]
        yield "str", self.value["str"]
        yield "bits", self.value["bits"]
        yield "integer", self.value["integer"]
        yield "realvalue", self.value["realvalue"]
        yield "children", self.value["children"]
        yield "attributes", self.value["attributes"]
        yield "dimensions", self.value["dimensions"]
        yield "location", self.value["location"]


class HashContainerPrinter:
    def __init__(self, value, kind):
        self.value = value
        self.kind = kind

    def to_string(self):
        return "{} with {} entries".format(self.kind, _dict_size(self.value))

    def children(self):
        entries = self.value["entries"]
        size = min(_vector_size(entries), _MAX_CHILDREN)
        for index in range(size):
            entry = _vector_at(entries, index)
            yield "[{}]".format(index), entry["udata"]
        if _vector_size(entries) > _MAX_CHILDREN:
            yield "<truncated>", "set $_yosys_gdb_max_children to inspect more"

    def display_hint(self):
        return "array"


class Factory:
    def __init__(self, printer, *args):
        self.printer = printer
        self.args = args

    def __call__(self, value):
        return self.printer(value, *self.args)


printers = gdb.printing.RegexpCollectionPrettyPrinter("yosys")
printers.add_printer("IdString", r"^Yosys::RTLIL::(Owning)?IdString$", IdStringPrinter)
printers.add_printer("Const", r"^Yosys::RTLIL::Const$", ConstPrinter)
printers.add_printer("SigBit", r"^Yosys::RTLIL::SigBit$", SigBitPrinter)
printers.add_printer("SigChunk", r"^Yosys::RTLIL::SigChunk$", SigChunkPrinter)
printers.add_printer("SigSpec", r"^Yosys::RTLIL::SigSpec$", SigSpecPrinter)
for kind in ("Wire", "Memory", "Cell", "Module", "Process"):
    printers.add_printer(kind, r"^Yosys::RTLIL::{}$".format(kind), Factory(NamedObjectPrinter, kind))
printers.add_printer("Design", r"^Yosys::RTLIL::Design$", DesignPrinter)
printers.add_printer("Selection", r"^Yosys::RTLIL::Selection$", SelectionPrinter)
printers.add_printer("CaseRule", r"^Yosys::RTLIL::CaseRule$", CaseRulePrinter)
printers.add_printer("SwitchRule", r"^Yosys::RTLIL::SwitchRule$", SwitchRulePrinter)
printers.add_printer("SyncRule", r"^Yosys::RTLIL::SyncRule$", SyncRulePrinter)
printers.add_printer("MemWriteAction", r"^Yosys::RTLIL::MemWriteAction$", MemWriteActionPrinter)
printers.add_printer("AstNode", r"^Yosys::AST::AstNode$", AstNodePrinter)
printers.add_printer("dict", r"^Yosys::hashlib::dict<.*>$", Factory(HashContainerPrinter, "dict"))
printers.add_printer("pool", r"^Yosys::hashlib::pool<.*>$", Factory(HashContainerPrinter, "pool"))
gdb.printing.register_pretty_printer(None, printers, replace=True)
end

import gdb
import gdb.printing
import sys

# /usr/share/gcc/python/libstdcxx/v6/printers.py
sys.path.insert(0, '/usr/share/gcc/python')
from libstdcxx.v6.printers import register_libstdcxx_printers
register_libstdcxx_printers (None)

class IdStringPrinter:
    _calling = False

    def __init__(self, value):
        self.value = value

    def display_hint(self):
        return "string"

    def to_string(self):
        index = int(self.value["index_"])
        if IdStringPrinter._calling or self.value.address is None:
            return f"<IdString index={index}>"

        # GDB's DAP adapter emits continued/stopped for inferior calls. Zed
        # refreshes variables on stopped, which otherwise calls us forever.
        dap_events = sys.modules.get("gdb.dap.events")
        dap_handler = getattr(dap_events, "_on_inferior_call", None)
        if dap_handler is not None:
            gdb.events.inferior_call.disconnect(dap_handler)

        try:
            IdStringPrinter._calling = True
            address = int(self.value.address)
            result = gdb.parse_and_eval(
                f"((const Yosys::RTLIL::IdString *)0x{address:x})->c_str()"
            )
            return result.string(errors="replace")
        except gdb.error as error:
            return f"<IdString index={index}: {error}>"
        finally:
            IdStringPrinter._calling = False
            if dap_handler is not None:
                gdb.events.inferior_call.connect(dap_handler)


printers = gdb.printing.RegexpCollectionPrettyPrinter("yosys")
printers.add_printer(
    "IdString", r"^Yosys::RTLIL::(?:Owning)?IdString$", IdStringPrinter
)
gdb.printing.register_pretty_printer(gdb.current_progspace(), printers, replace=True)

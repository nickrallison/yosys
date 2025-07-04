set(YOSYS_PASSES_PROC_SOURCES
    proc.cc
    proc_prune.cc
    proc_clean.cc
    proc_rmdead.cc
    proc_init.cc
    proc_arst.cc
    proc_rom.cc
    proc_mux.cc
    proc_dlatch.cc
    proc_dff.cc
    proc_memwr.cc
)

add_library(Yosys::Passes::Proc OBJECT
  ${YOSYS_PASSES_PROC_SOURCES}
)

target_link_libraries(Yosys::Passes::Proc
  PUBLIC Yosys::Interface
)
set(YOSYS_PASSES_EQUIV_SOURCES
    equiv_make.cc
    equiv_miter.cc
    equiv_simple.cc
    equiv_status.cc
    equiv_add.cc
    equiv_remove.cc
    equiv_induct.cc
    equiv_struct.cc
    equiv_purge.cc
    equiv_mark.cc
    equiv_opt.cc
)

add_library(Yosys::Passes::Equiv OBJECT
  ${YOSYS_PASSES_EQUIV_SOURCES}
)

target_link_libraries(Yosys::Passes::Equiv
  PUBLIC
    Yosys::Interface
)
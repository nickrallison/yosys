set(YOSYS_BACKENDS_AIGER_SOURCES
    aiger.cc
    xaiger.cc
)

add_library(Yosys::Backends::Aiger OBJECT
  ${YOSYS_BACKENDS_AIGER_SOURCES}
)

target_link_libraries(Yosys::Backends::Aiger
  PUBLIC
    Yosys::Interface
)

add_library(Yosys::Backends::SimpleC OBJECT
    simplec.cc
)

target_link_libraries(Yosys::Backends::SimpleC
  PUBLIC
    Yosys::Interface
)
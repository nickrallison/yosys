add_library(Yosys::Backends::Firrtl OBJECT
  firrtl.cc
)

target_link_libraries(Yosys::Backends::Firrtl
  PUBLIC
    Yosys::Interface
)

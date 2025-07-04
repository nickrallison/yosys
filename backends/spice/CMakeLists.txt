add_library(Yosys::Backends::Spice OBJECT
  spice.cc
)

target_link_libraries(Yosys::Backends::Spice
  PUBLIC
    Yosys::Interface
)
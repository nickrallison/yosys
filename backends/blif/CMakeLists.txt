add_library(Yosys::Backends::Blif OBJECT
    blif.cc
)

target_link_libraries(Yosys::Backends::Blif
  PUBLIC
    Yosys::Interface
)
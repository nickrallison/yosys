add_library(Yosys::Backends::Edif OBJECT
    edif.cc
)

target_link_libraries(Yosys::Backends::Edif
  PUBLIC
    Yosys::Interface
)
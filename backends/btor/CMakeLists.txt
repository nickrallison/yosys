add_library(Yosys::Backends::Btor OBJECT
  btor.cc
)

target_link_libraries(Yosys::Backends::Btor
  PUBLIC
    Yosys::Interface
)
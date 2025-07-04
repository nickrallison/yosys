add_library(Yosys::Backends::Smv OBJECT
  smv.cc
)

target_link_libraries(Yosys::Backends::Smv
  PUBLIC
    Yosys::Interface
)

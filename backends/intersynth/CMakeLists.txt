add_library(Yosys::Backends::Intersynth OBJECT
  intersynth.cc
)

target_link_libraries(Yosys::Backends::Intersynth
  PUBLIC
    Yosys::Interface
)
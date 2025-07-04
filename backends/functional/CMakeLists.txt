add_library(Yosys::Backends::Functional OBJECT
    cxx.cc
    smtlib.cc
    smtlib_rosette.cc
    test_generic.cc
)

target_link_libraries(Yosys::Backends::Functional
  PUBLIC
    Yosys::Interface
)

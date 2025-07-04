add_library(Yosys::Backends::Smt2 OBJECT
  smt2.cc
)

target_link_libraries(Yosys::Backends::Smt2
  PUBLIC
    Yosys::Interface
)

add_share_file("share/python3" "smtio.py")
add_share_file("share/python3" "ywio.py")

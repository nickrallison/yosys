set(YOSYS_PASSES_TESTS_SOURCES
  test_autotb.cc
  test_cell.cc
  test_abcloop.cc
)

add_library(Yosys::Passes::Tests OBJECT
  ${YOSYS_PASSES_TESTS_SOURCES}
)

target_link_libraries(Yosys::Passes::Tests
  PUBLIC
    Yosys::Interface
)
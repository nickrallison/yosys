cmake_minimum_required(VERSION 3.23)
project(yosys_passes_tests LANGUAGES CXX)

add_library(${PROJECT_NAME})

target_sources(${PROJECT_NAME} PRIVATE
    test_autotb.cc
    test_cell.cc
    test_abcloop.cc
)

target_link_libraries(${PROJECT_NAME}
    PUBLIC
        yosys_kernel
)
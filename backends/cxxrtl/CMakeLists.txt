cmake_minimum_required(VERSION 3.23)
project(yosys_backends_cxxrtl LANGUAGES CXX)

add_library(${PROJECT_NAME})

target_sources(${PROJECT_NAME} PRIVATE
    cxxrtl_backend.cc
)

target_link_libraries(${PROJECT_NAME}
    PUBLIC
        yosys_kernel
)

add_include_file("backends/cxxrtl/runtime/cxxrtl" "runtime/cxxrtl/cxxrtl.h")
add_include_file("backends/cxxrtl/runtime/cxxrtl" "runtime/cxxrtl/cxxrtl_vcd.h")
add_include_file("backends/cxxrtl/runtime/cxxrtl" "runtime/cxxrtl/cxxrtl_time.h")
add_include_file("backends/cxxrtl/runtime/cxxrtl" "runtime/cxxrtl/cxxrtl_replay.h")
add_include_file("backends/cxxrtl/runtime/cxxrtl/capi" "runtime/cxxrtl/capi/cxxrtl_capi.cc")
add_include_file("backends/cxxrtl/runtime/cxxrtl/capi" "runtime/cxxrtl/capi/cxxrtl_capi.h")
add_include_file("backends/cxxrtl/runtime/cxxrtl/capi" "runtime/cxxrtl/capi/cxxrtl_capi_vcd.cc")
add_include_file("backends/cxxrtl/runtime/cxxrtl/capi" "runtime/cxxrtl/capi/cxxrtl_capi_vcd.h")

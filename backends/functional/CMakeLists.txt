cmake_minimum_required(VERSION 3.23)
project(yosys_backends_functional LANGUAGES CXX)

add_library(${PROJECT_NAME})

target_sources(${PROJECT_NAME} PRIVATE
    cxx.cc
    smtlib.cc
    smtlib_rosette.cc
    test_generic.cc
)

target_link_libraries(${PROJECT_NAME}
    PUBLIC
        yosys_kernel
)

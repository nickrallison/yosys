cmake_minimum_required(VERSION 3.23)
project(yosys_techlibs_fabulous LANGUAGES CXX)

add_library(${PROJECT_NAME})

target_sources(${PROJECT_NAME} PRIVATE
    synth_fabulous.cc
)

target_link_libraries(${PROJECT_NAME}
    PUBLIC
        yosys_kernel
)

add_share_file("share/fabulous" "cells_map.v")
add_share_file("share/fabulous" "prims.v")
add_share_file("share/fabulous" "latches_map.v")
add_share_file("share/fabulous" "ff_map.v")
add_share_file("share/fabulous" "ram_regfile.txt")
add_share_file("share/fabulous" "regfile_map.v")
add_share_file("share/fabulous" "io_map.v")
add_share_file("share/fabulous" "arith_map.v")

cmake_minimum_required(VERSION 3.23)
project(yosys_techlibs_sf2 LANGUAGES CXX)

add_library(${PROJECT_NAME})

target_sources(${PROJECT_NAME} PRIVATE
    synth_sf2.cc
)

target_link_libraries(${PROJECT_NAME}
    PUBLIC
        yosys_kernel
)

add_share_file("share/sf2" "arith_map.v")
add_share_file("share/sf2" "cells_map.v")
add_share_file("share/sf2" "cells_sim.v")

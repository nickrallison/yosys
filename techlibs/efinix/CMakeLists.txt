cmake_minimum_required(VERSION 3.23)
project(yosys_techlibs_efinix LANGUAGES CXX)

add_library(${PROJECT_NAME})

target_sources(${PROJECT_NAME} PRIVATE
    synth_efinix.cc
    efinix_fixcarry.cc
)

target_link_libraries(${PROJECT_NAME}
    PUBLIC
        yosys_kernel
)


add_share_file("share/efinix" "cells_map.v")
add_share_file("share/efinix" "arith_map.v")
add_share_file("share/efinix" "cells_sim.v")
add_share_file("share/efinix" "brams_map.v")
add_share_file("share/efinix" "gbuf_map.v")
add_share_file("share/efinix" "brams.txt")

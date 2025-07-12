cmake_minimum_required(VERSION 3.23)
project(yosys_techlibs_nexus LANGUAGES CXX)

add_library(${PROJECT_NAME})

target_sources(${PROJECT_NAME} PRIVATE
    synth_nexus.cc
)

target_link_libraries(${PROJECT_NAME}
    PUBLIC
        yosys_kernel
)

add_share_file("share/nexus" "cells_map.v")
add_share_file("share/nexus" "cells_sim.v")
add_share_file("share/nexus" "parse_init.vh")
add_share_file("share/nexus" "cells_xtra.v")
add_share_file("share/nexus" "lutrams_map.v")
add_share_file("share/nexus" "lutrams.txt")
add_share_file("share/nexus" "brams_map.v")
add_share_file("share/nexus" "brams.txt")
add_share_file("share/nexus" "lrams_map.v")
add_share_file("share/nexus" "lrams.txt")
add_share_file("share/nexus" "arith_map.v")
add_share_file("share/nexus" "latches_map.v")
add_share_file("share/nexus" "dsp_map.v")

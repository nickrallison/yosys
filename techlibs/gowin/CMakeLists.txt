cmake_minimum_required(VERSION 3.23)
project(yosys_techlibs_gowin LANGUAGES CXX)

add_library(${PROJECT_NAME})

target_sources(${PROJECT_NAME} PRIVATE
    synth_gowin.cc
)

target_link_libraries(${PROJECT_NAME}
    PUBLIC
        yosys_kernel
)

add_share_file("share/gowin" "cells_map.v")
add_share_file("share/gowin" "cells_sim.v")
add_share_file("share/gowin" "cells_xtra_gw1n.v")
add_share_file("share/gowin" "cells_xtra_gw2a.v")
add_share_file("share/gowin" "cells_xtra_gw5a.v")
add_share_file("share/gowin" "arith_map.v")
add_share_file("share/gowin" "brams_map.v")
add_share_file("share/gowin" "brams.txt")
add_share_file("share/gowin" "lutrams_map.v")
add_share_file("share/gowin" "lutrams.txt")

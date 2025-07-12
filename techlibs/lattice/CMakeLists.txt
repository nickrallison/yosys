cmake_minimum_required(VERSION 3.23)
project(yosys_techlibs_lattice LANGUAGES CXX)

add_library(${PROJECT_NAME})

target_sources(${PROJECT_NAME} PRIVATE
    synth_lattice.cc
    lattice_gsr.cc
)

target_link_libraries(${PROJECT_NAME}
    PUBLIC
        yosys_kernel
)

add_share_file("share/lattice" "cells_ff.vh")
add_share_file("share/lattice" "cells_io.vh")
add_share_file("share/lattice" "cells_map.v")
add_share_file("share/lattice" "common_sim.vh")
add_share_file("share/lattice" "ccu2d_sim.vh")
add_share_file("share/lattice" "ccu2c_sim.vh")
add_share_file("share/lattice" "cells_sim_ecp5.v")
add_share_file("share/lattice" "cells_sim_xo2.v")
add_share_file("share/lattice" "cells_sim_xo3.v")
add_share_file("share/lattice" "cells_sim_xo3d.v")
add_share_file("share/lattice" "cells_bb_ecp5.v")
add_share_file("share/lattice" "cells_bb_xo2.v")
add_share_file("share/lattice" "cells_bb_xo3.v")
add_share_file("share/lattice" "cells_bb_xo3d.v")
add_share_file("share/lattice" "lutrams_map.v")
add_share_file("share/lattice" "lutrams.txt")
add_share_file("share/lattice" "brams_map_16kd.v")
add_share_file("share/lattice" "brams_16kd.txt")
add_share_file("share/lattice" "brams_map_8kc.v")
add_share_file("share/lattice" "brams_8kc.txt")
add_share_file("share/lattice" "arith_map_ccu2c.v")
add_share_file("share/lattice" "arith_map_ccu2d.v")
add_share_file("share/lattice" "latches_map.v")
add_share_file("share/lattice" "dsp_map_18x18.v")

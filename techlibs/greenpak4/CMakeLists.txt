cmake_minimum_required(VERSION 3.23)
project(yosys_techlibs_greenpak4 LANGUAGES CXX)

add_library(${PROJECT_NAME})

target_sources(${PROJECT_NAME} PRIVATE
    synth_greenpak4.cc
    greenpak4_dffinv.cc
)

target_link_libraries(${PROJECT_NAME}
    PUBLIC
        yosys_kernel
)

add_share_file("share/greenpak4" "cells_blackbox.v")
add_share_file("share/greenpak4" "cells_latch.v")
add_share_file("share/greenpak4" "cells_map.v")
add_share_file("share/greenpak4" "cells_sim.v")
add_share_file("share/greenpak4" "cells_sim_ams.v")
add_share_file("share/greenpak4" "cells_sim_digital.v")
add_share_file("share/greenpak4" "cells_sim_wip.v")
add_share_file("share/greenpak4" "gp_dff.lib")

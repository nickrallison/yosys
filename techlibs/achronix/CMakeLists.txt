cmake_minimum_required(VERSION 3.23)
project(yosys_techlibs_achronix LANGUAGES CXX)

add_library(${PROJECT_NAME})
target_sources(${PROJECT_NAME} PRIVATE
    synth_achronix.cc
)

target_link_libraries(${PROJECT_NAME}
    PUBLIC
        yosys_kernel
)

add_share_file("share/achronix/speedster22i" "speedster22i/cells_sim.v")
add_share_file("share/achronix/speedster22i" "speedster22i/cells_map.v")

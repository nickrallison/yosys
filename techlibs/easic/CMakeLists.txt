cmake_minimum_required(VERSION 3.23)
project(yosys_techlibs_easic LANGUAGES CXX)

add_library(${PROJECT_NAME})

target_sources(${PROJECT_NAME} PRIVATE
    synth_easic.cc
)

target_link_libraries(${PROJECT_NAME}
    PUBLIC
        yosys_kernel
)

cmake_minimum_required(VERSION 3.23)
project(yosys_passes_equiv LANGUAGES CXX)

add_library(${PROJECT_NAME})

target_sources(${PROJECT_NAME} PRIVATE
    equiv_make.cc
    equiv_miter.cc
    equiv_simple.cc
    equiv_status.cc
    equiv_add.cc
    equiv_remove.cc
    equiv_induct.cc
    equiv_struct.cc
    equiv_purge.cc
    equiv_mark.cc
    equiv_opt.cc
)

target_link_libraries(${PROJECT_NAME}
    PUBLIC
        yosys_kernel
)


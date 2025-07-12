cmake_minimum_required(VERSION 3.23)
project(yosys_passes_proc LANGUAGES CXX)

add_library(${PROJECT_NAME})

target_sources(${PROJECT_NAME} PRIVATE
    proc.cc
    proc_prune.cc
    proc_clean.cc
    proc_rmdead.cc
    proc_init.cc
    proc_arst.cc
    proc_rom.cc
    proc_mux.cc
    proc_dlatch.cc
    proc_dff.cc
    proc_memwr.cc
)

target_link_libraries(${PROJECT_NAME} PUBLIC
    yosys_kernel
)

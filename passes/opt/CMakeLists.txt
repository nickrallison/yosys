cmake_minimum_required(VERSION 3.23)
project(yosys_passes_opt LANGUAGES CXX)

add_library(${PROJECT_NAME})
target_sources(${PROJECT_NAME} PRIVATE
    opt.cc
    opt_merge.cc
    opt_mem.cc
    opt_mem_feedback.cc
    opt_mem_priority.cc
    opt_mem_widen.cc
    opt_muxtree.cc
    opt_reduce.cc
    opt_dff.cc
    opt_share.cc
    opt_clean.cc
    opt_expr.cc
    share.cc
    wreduce.cc
    opt_demorgan.cc
    rmports.cc
    opt_lut.cc
    opt_lut_ins.cc
    opt_ffinv.cc
    pmux2shiftx.cc
    muxpack.cc
)

target_link_libraries(${PROJECT_NAME}
    PUBLIC
        yosys_kernel
)
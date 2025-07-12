cmake_minimum_required(VERSION 3.23)
project(yosys_passes_sat LANGUAGES CXX)

add_library(${PROJECT_NAME})

target_sources(${PROJECT_NAME} PRIVATE
    sat.cc
    freduce.cc
    eval.cc
    miter.cc
    expose.cc
    assertpmux.cc
    clk2fflogic.cc
    async2sync.cc
    formalff.cc
    supercover.cc
    fmcombine.cc
    mutate.cc
    cutpoint.cc
    fminit.cc
    recover_names.cc
    synthprop.cc

)

if (ENABLE_ZLIB)
target_sources(${PROJECT_NAME} PRIVATE
    sim.cc
)
endif()

if (NOT DISABLE_SPAWN)
target_sources(${PROJECT_NAME} PRIVATE
    qbfsat.cc
)
endif()

target_link_libraries(${PROJECT_NAME}
    PUBLIC
        yosys_kernel
)

target_include_directories(${PROJECT_NAME}
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
        $<BUILD_INTERFACE:${yosys_SOURCE_DIR}>
        $<INSTALL_INTERFACE:include>
)

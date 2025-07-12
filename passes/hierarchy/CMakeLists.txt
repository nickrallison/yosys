cmake_minimum_required(VERSION 3.23)
project(yosys_passes_hierarchy LANGUAGES CXX)

add_library(${PROJECT_NAME})
target_sources(${PROJECT_NAME} PRIVATE
    hierarchy.cc
    uniquify.cc
    submod.cc
    keep_hierarchy.cc
)

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

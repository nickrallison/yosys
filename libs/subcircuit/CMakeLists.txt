cmake_minimum_required(VERSION 3.23)
project(yosys_libs_subcircuit LANGUAGES CXX)

add_library(${PROJECT_NAME})
target_sources(
    ${PROJECT_NAME}
    PRIVATE
        subcircuit.cc

    PUBLIC
    FILE_SET HEADERS
    BASE_DIRS .
    FILES
        subcircuit.h
)

target_include_directories(${PROJECT_NAME}
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
        $<INSTALL_INTERFACE:include>
)

add_library(subcircuit ALIAS ${PROJECT_NAME})
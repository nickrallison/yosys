cmake_minimum_required(VERSION 3.23)
project(yosys_passes_memory LANGUAGES CXX)

add_library(${PROJECT_NAME})
target_sources(
    ${PROJECT_NAME}
    PRIVATE
        memory.cc
        memory_dff.cc
        memory_share.cc
        memory_collect.cc
        memory_unpack.cc
        memory_bram.cc
        memory_map.cc
        memory_memx.cc
        memory_nordff.cc
        memory_narrow.cc
        memory_libmap.cc
        memory_bmux2rom.cc
        memlib.cc
    PUBLIC
    FILE_SET HEADERS
    BASE_DIRS .
    FILES
        memlib.h
)

target_link_libraries(${PROJECT_NAME}
    PUBLIC
        yosys_kernel
)

target_include_directories(${PROJECT_NAME}
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
        $<INSTALL_INTERFACE:include>
)

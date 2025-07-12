cmake_minimum_required(VERSION 3.23)
project(yosys_passes_fsm LANGUAGES CXX)

add_library(${PROJECT_NAME})
target_sources(
    ${PROJECT_NAME}
    PRIVATE
        fsm.cc
        fsm_detect.cc
        fsm_extract.cc
        fsm_opt.cc
        fsm_expand.cc
        fsm_recode.cc
        fsm_info.cc
        fsm_export.cc
        fsm_map.cc
    PUBLIC
    FILE_SET HEADERS
    BASE_DIRS .
    FILES
        fsmdata.h
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

cmake_minimum_required(VERSION 3.23)
project(yosys_libs_ezsat LANGUAGES CXX)

add_library(${PROJECT_NAME})
target_sources(
    ${PROJECT_NAME}
    PRIVATE
        ezminisat.cc
        ezsat.cc

    PUBLIC
    FILE_SET HEADERS
    BASE_DIRS .
    FILES
        ezminisat.h
        ezsat.h
)

target_link_libraries(${PROJECT_NAME}
    PUBLIC
        minisat
)

target_include_directories(${PROJECT_NAME}
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
        $<INSTALL_INTERFACE:include>
)

add_library(ezsat ALIAS ${PROJECT_NAME})
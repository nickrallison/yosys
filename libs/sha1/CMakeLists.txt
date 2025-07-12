cmake_minimum_required(VERSION 3.23)
project(yosys_libs_sha1 LANGUAGES CXX)

add_library(${PROJECT_NAME}
   sha1.cpp
)

target_include_directories(${PROJECT_NAME} PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
    $<INSTALL_INTERFACE:include>
)

target_include_directories(${PROJECT_NAME}
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
        $<INSTALL_INTERFACE:include>
)

add_library(sha1 ALIAS ${PROJECT_NAME})
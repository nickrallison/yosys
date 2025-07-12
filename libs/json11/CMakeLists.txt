cmake_minimum_required(VERSION 3.23)
project(yosys_libs_json11 LANGUAGES CXX)

add_library(${PROJECT_NAME}
   json11.cpp
)

target_include_directories(${PROJECT_NAME} PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
    $<INSTALL_INTERFACE:include>
)
add_library(json11 ALIAS ${PROJECT_NAME})
cmake_minimum_required(VERSION 3.23)
project(yosys_backends_btor LANGUAGES CXX)

add_library(${PROJECT_NAME})

target_sources(${PROJECT_NAME} PRIVATE
    btor.cc
)

target_link_libraries(${PROJECT_NAME}
    PUBLIC
        yosys_kernel
)
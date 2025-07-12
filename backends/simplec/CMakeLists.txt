cmake_minimum_required(VERSION 3.23)
project(yosys_backends_simplec LANGUAGES CXX)

add_library(${PROJECT_NAME})

target_sources(${PROJECT_NAME} PRIVATE
    simplec.cc
)

target_link_libraries(${PROJECT_NAME}
    PUBLIC
        yosys_kernel
)
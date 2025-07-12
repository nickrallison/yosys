cmake_minimum_required(VERSION 3.23)
project(yosys_frontends_aiger2 LANGUAGES CXX)

add_library(${PROJECT_NAME})

target_sources(${PROJECT_NAME} PRIVATE
    xaiger.cc
)

target_link_libraries(${PROJECT_NAME}
    PUBLIC
        yosys_kernel
)
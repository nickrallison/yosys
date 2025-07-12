cmake_minimum_required(VERSION 3.23)
project(yosys_backends_smt2 LANGUAGES CXX)

add_library(${PROJECT_NAME})

target_sources(${PROJECT_NAME} PRIVATE
    smt2.cc
)

target_link_libraries(${PROJECT_NAME}
    PUBLIC
        yosys_kernel
)

add_share_file("share/python3" "smtio.py")
add_share_file("share/python3" "ywio.py")

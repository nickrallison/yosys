cmake_minimum_required(VERSION 3.23)
project(yosys_frontends_rpc LANGUAGES CXX)

add_library(${PROJECT_NAME})

target_sources(${PROJECT_NAME} PRIVATE
    rpc_frontend.cc
)

target_link_libraries(${PROJECT_NAME}
    PUBLIC
        json11

        yosys_kernel
)

target_include_directories(${PROJECT_NAME}
    PUBLIC
        $<BUILD_INTERFACE:${yosys_SOURCE_DIR}>
        $<INSTALL_INTERFACE:include>
)


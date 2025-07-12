cmake_minimum_required(VERSION 3.23)
project(yosys_frontends_ast LANGUAGES CXX)

add_library(${PROJECT_NAME})
target_sources(
    ${PROJECT_NAME}
    PRIVATE
        ast_binding.cc
        ast.cc
        dpicall.cc
        genrtlil.cc
        simplify.cc
    PUBLIC
    FILE_SET HEADERS
    BASE_DIRS .
    FILES
        ast_binding.h
        ast.h
)

target_link_libraries(${PROJECT_NAME} PUBLIC yosys_kernel)

target_include_directories(${PROJECT_NAME}
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
        $<INSTALL_INTERFACE:include>
)
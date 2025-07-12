cmake_minimum_required(VERSION 3.23)
project(yosys_frontends_verilog LANGUAGES CXX)

add_custom_command(
    OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/frontends_verilog_dir
    COMMAND ${CMAKE_COMMAND} -E make_directory ${yosys_BINARY_DIR}/frontends/verilog
    COMMAND ${CMAKE_COMMAND} -E touch ${CMAKE_CURRENT_BINARY_DIR}/frontends_verilog_dir
    COMMENT "Creating frontends/verilog directory"
)

add_custom_target(frontends_verilog_dir_target DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/frontends_verilog_dir)

flex_target(VERILOG_LEXER "${yosys_SOURCE_DIR}/frontends/verilog/verilog_lexer.l" "${yosys_BINARY_DIR}/frontends/verilog/verilog_lexer.cc")
bison_target(VERILOG_PARSER "${yosys_SOURCE_DIR}/frontends/verilog/verilog_parser.y" "${yosys_BINARY_DIR}/frontends/verilog/verilog_parser.tab.cc" DEFINES_FILE "${yosys_BINARY_DIR}/frontends/verilog/verilog_parser.tab.hh" COMPILE_FLAGS "-Wall -Werror -d -r all")

add_library(${PROJECT_NAME} STATIC)
target_sources(${PROJECT_NAME} PRIVATE
    ${yosys_SOURCE_DIR}/frontends/verilog/const2ast.cc
    ${yosys_SOURCE_DIR}/frontends/verilog/preproc.cc
    ${yosys_SOURCE_DIR}/frontends/verilog/preproc.h
    ${yosys_SOURCE_DIR}/frontends/verilog/verilog_frontend.cc
    ${yosys_SOURCE_DIR}/frontends/verilog/verilog_frontend.h
)

target_sources(${PROJECT_NAME} PRIVATE
    ${FLEX_VERILOG_LEXER_OUTPUTS}
    ${BISON_VERILOG_PARSER_OUTPUTS}
)

add_dependencies(${PROJECT_NAME} frontends_verilog_dir_target)

target_include_directories(${PROJECT_NAME}
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
        $<BUILD_INTERFACE:${yosys_SOURCE_DIR}>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
        $<BUILD_INTERFACE:${yosys_BINARY_DIR}>
        $<INSTALL_INTERFACE:include>
)

target_link_libraries(${PROJECT_NAME} PUBLIC
    yosys_frontends_ast
    yosys_kernel
)

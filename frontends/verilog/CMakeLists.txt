flex_target(VERILOG_LEXER "verilog_lexer.l" "${CMAKE_CURRENT_BINARY_DIR}/verilog_lexer.cc")
bison_target(VERILOG_PARSER "verilog_parser.y" "${CMAKE_CURRENT_BINARY_DIR}/verilog_parser.tab.cc" DEFINES_FILE "${CMAKE_CURRENT_BINARY_DIR}/verilog_parser.tab.hh" COMPILE_FLAGS "-Wall -Werror -d -r all")

add_custom_target(yosys_frontends_verilog_gen DEPENDS
    ${FLEX_VERILOG_LEXER_OUTPUTS}
    ${BISON_VERILOG_PARSER_OUTPUTS}
)

add_library(yosys_frontends_verilog INTERFACE
    const2ast.cc
    preproc.cc
    verilog_frontend.cc
    ${FLEX_VERILOG_LEXER_OUTPUTS}
    ${BISON_VERILOG_PARSER_OUTPUTS}
)

add_dependencies(yosys_frontends_verilog yosys_frontends_verilog_gen)

target_include_directories(yosys_frontends_verilog
    INTERFACE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
        $<INSTALL_INTERFACE:include>
)

target_link_libraries(yosys_kernel INTERFACE yosys_frontends_verilog)
# target_link_libraries(yosys_frontends_verilog INTERFACEyosys_kernel)


flex_target(VERILOG_LEXER "verilog_lexer.l" "${CMAKE_CURRENT_BINARY_DIR}/verilog_lexer.cc")
bison_target(VERILOG_PARSER "verilog_parser.y" "${CMAKE_CURRENT_BINARY_DIR}/verilog_parser.tab.cc" DEFINES_FILE "${CMAKE_CURRENT_BINARY_DIR}/verilog_parser.tab.hh" COMPILE_FLAGS "-Wall -Werror -d -r all")


add_library(yosys_frontends_verilog STATIC
    const2ast.cc
    preproc.cc
    preproc.h
    verilog_frontend.cc
    verilog_frontend.h
)

add_library(yosys_frontends_verilog_gen STATIC
    ${FLEX_VERILOG_LEXER_OUTPUTS}
    ${BISON_VERILOG_PARSER_OUTPUTS}
    #${CMAKE_CURRENT_BINARY_DIR}/verilog_lexer.cc
    #${CMAKE_CURRENT_BINARY_DIR}/verilog_parser.tab.cc
    #${CMAKE_CURRENT_BINARY_DIR}/verilog_parser.tab.hh
)
target_link_libraries(yosys_obj PUBLIC yosys_frontends_verilog yosys_frontends_verilog_gen)
target_link_libraries(yosys_frontends_verilog_gen PUBLIC yosys_kernel)
target_link_libraries(yosys_frontends_verilog PUBLIC yosys_kernel)


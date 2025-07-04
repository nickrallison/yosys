flex_target(VERILOG_LEXER "verilog_lexer.l" "${CMAKE_CURRENT_BINARY_DIR}/verilog_lexer.cc")
bison_target(VERILOG_PARSER "verilog_parser.y"
    "${CMAKE_CURRENT_BINARY_DIR}/verilog_parser.tab.cc"
    DEFINES_FILE "${CMAKE_CURRENT_BINARY_DIR}/verilog_parser.tab.hh"
    COMPILE_FLAGS "-Wall -Werror -d -r all"
)

add_library(Yosys::Frontends::VerilogGen OBJECT
    ${FLEX_VERILOG_LEXER_OUTPUTS}
    ${BISON_VERILOG_PARSER_OUTPUTS}
)

target_link_libraries(Yosys::Frontends::VerilogGen
  PUBLIC
    Yosys::Interface
)

set(YOSYS_FRONTENDS_VERILOG_SOURCES
    const2ast.cc
    preproc.cc
    verilog_frontend.cc
)

set(YOSYS_FRONTENDS_VERILOG_HEADERS
    preproc.h
    verilog_frontend.h
)

add_library(Yosys::Frontends::Verilog OBJECT
  ${YOSYS_FRONTENDS_VERILOG_SOURCES}
)

target_sources(Yosys::Frontends::Verilog
  FILE_SET HEADERS
    TYPE    HEADERS
    BASE_DIR ${CMAKE_CURRENT_SOURCE_DIR}
    FILES   ${YOSYS_FRONTENDS_VERILOG_HEADERS}
)

target_link_libraries(Yosys::Frontends::Verilog
  PUBLIC
    Yosys::Interface
)

install(
  TARGETS Yosys::Frontends::Verilog
  FILE_SET HEADERS DESTINATION frontends/verilog
)

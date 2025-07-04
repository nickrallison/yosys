flex_target(RTLIL_LEXER "rtlil_lexer.l" "${CMAKE_CURRENT_BINARY_DIR}/rtlil_lexer.cc")
bison_target(RTLIL_PARSER "rtlil_parser.y" "${CMAKE_CURRENT_BINARY_DIR}/rtlil_parser.tab.cc" DEFINES_FILE "${CMAKE_CURRENT_BINARY_DIR}/rtlil_parser.tab.hh" COMPILE_FLAGS "-d -r all")

add_library(Yosys::Frontends::Rtlil OBJECT
    rtlil_frontend.cc)

add_library(Yosys::Frontends::RtlilGen OBJECT
    ${FLEX_RTLIL_LEXER_OUTPUTS}
    ${BISON_RTLIL_PARSER_OUTPUTS}
)

target_link_libraries(Yosys::Frontends::Rtlil
  PUBLIC
    Yosys::Interface
)
target_link_libraries(Yosys::Frontends::RtlilGen
  PUBLIC
    Yosys::Interface
)
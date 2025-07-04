set(YOSYS_FRONTENDS_AST_SOURCES
    ast_binding.cc
    ast.cc
    dpicall.cc
    genrtlil.cc
    simplify.cc
)

set(YOSYS_FRONTENDS_AST_HEADERS
    ast_binding.h
    ast.h
)

add_library(Yosys::Frontends::Ast OBJECT
  ${YOSYS_FRONTENDS_AST_SOURCES}
)

target_sources(Yosys::Frontends::Ast
  FILE_SET HEADERS
    TYPE    HEADERS
    BASE_DIR ${CMAKE_CURRENT_SOURCE_DIR}
    FILES   ${YOSYS_FRONTENDS_AST_HEADERS}
)

target_link_libraries(Yosys::Frontends::Ast
  PUBLIC
    Yosys::Interface
)

install(
  TARGETS Yosys::Frontends::Ast
  FILE_SET HEADERS DESTINATION frontends/ast
)
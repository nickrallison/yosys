set(YOSYS_FRONTENDS_AIGER_SOURCES
    aigerparse.cc
)

set(YOSYS_FRONTENDS_AIGER_HEADERS
    aigerparse.h
)

add_library(Yosys::Frontends::Aiger OBJECT
  ${YOSYS_FRONTENDS_AIGER_SOURCES}
)

target_sources(Yosys::Frontends::Aiger
  FILE_SET HEADERS
    TYPE    HEADERS
    BASE_DIR ${CMAKE_CURRENT_SOURCE_DIR}
    FILES   ${YOSYS_FRONTENDS_AIGER_HEADERS}
)

target_link_libraries(Yosys::Frontends::Aiger PUBLIC Yosys::Interface)

install(
  TARGETS Yosys::Frontends::Aiger
  FILE_SET HEADERS DESTINATION frontends/aiger
)
set(YOSYS_FRONTENDS_BLIF_SOURCES
    blifparse.cc
)

set(YOSYS_FRONTENDS_BLIF_HEADERS
    blifparse.h
)

add_library(Yosys::Frontends::Blif OBJECT
  ${YOSYS_FRONTENDS_BLIF_SOURCES}
)

target_sources(Yosys::Frontends::Blif
  FILE_SET HEADERS
    TYPE    HEADERS
    BASE_DIR ${CMAKE_CURRENT_SOURCE_DIR}
    FILES   ${YOSYS_FRONTENDS_BLIF_HEADERS}
)

target_link_libraries(Yosys::Frontends::Blif PUBLIC Yosys::Interface)

install(
  TARGETS Yosys::Frontends::Blif
  FILE_SET HEADERS DESTINATION frontends/blif
)
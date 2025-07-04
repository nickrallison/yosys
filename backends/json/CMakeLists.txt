add_library(Yosys::Backends::Json OBJECT
  json.cc
)

target_sources(Yosys::Backends::Json
  FILE_SET HEADERS
    TYPE    HEADERS
    BASE_DIR ${CMAKE_CURRENT_SOURCE_DIR}
    FILES   json.h
)

target_link_libraries(Yosys::Backends::Json
  PUBLIC
    Yosys::Interface
)

install(
  TARGETS Yosys::Backends::Json
  FILE_SET HEADERS DESTINATION backends/json
)
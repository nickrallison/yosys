add_library(Yosys::Backends::Rtlil OBJECT
  rtlil_backend.cc
)

target_sources(Yosys::Backends::Rtlil
  FILE_SET HEADERS
    TYPE    HEADERS
    BASE_DIR ${CMAKE_CURRENT_SOURCE_DIR}
    FILES   rtlil_backend.h
)

target_link_libraries(Yosys::Backends::Rtlil
  PUBLIC
    Yosys::Interface
)

install(
  TARGETS Yosys::Backends::Rtlil
  FILE_SET HEADERS
    DESTINATION backends/rtlil
)
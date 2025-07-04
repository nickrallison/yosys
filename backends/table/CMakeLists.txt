add_library(Yosys::Backends::Verilog OBJECT
  verilog_backend.cc
)

target_sources(Yosys::Backends::Verilog
  FILE_SET HEADERS
    TYPE    HEADERS
    BASE_DIR ${CMAKE_CURRENT_SOURCE_DIR}
    FILES   
      verilog_backend.h
)

target_link_libraries(Yosys::Backends::Verilog
  PUBLIC
    Yosys::Interface
)

install(
  TARGETS Yosys::Backends::Verilog
  FILE_SET HEADERS
    DESTINATION backends/verilog
)
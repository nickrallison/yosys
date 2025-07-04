set(YOSYS_BACKENDS_CXXRTL_SOURCES
    cxxrtl_backend.cc
    runtime/cxxrtl/capi/cxxrtl_capi.cc
    runtime/cxxrtl/capi/cxxrtl_capi_vcd.cc
)

set(YOSYS_BACKENDS_CXXRTL_HEADERS
    runtime/cxxrtl/cxxrtl.h
    runtime/cxxrtl/cxxrtl_vcd.h
    runtime/cxxrtl/cxxrtl_time.h
    runtime/cxxrtl/cxxrtl_replay.h
    runtime/cxxrtl/capi/cxxrtl_capi.h
    runtime/cxxrtl/capi/cxxrtl_capi_vcd.h
)

add_library(Yosys::Backends::Cxxrtl
    OBJECT
    ${YOSYS_BACKENDS_CXXRTL_SOURCES}
)

target_sources(Yosys::Backends::Cxxrtl
  FILE_SET HEADERS
    TYPE    HEADERS
    BASE_DIR ${CMAKE_CURRENT_SOURCE_DIR}
    FILES   ${YOSYS_BACKENDS_CXXRTL_HEADERS}
)

target_link_libraries(Yosys::Backends::Cxxrtl
  PUBLIC
    Yosys::Interface
)

install(
  TARGETS Yosys::Backends::Cxxrtl
  FILE_SET HEADERS
    DESTINATION backends/cxxrtl
)

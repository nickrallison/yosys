set(YOSYS_PASSES_MEMORY_SOURCES
    memory.cc
    memory_dff.cc
    memory_share.cc
    memory_collect.cc
    memory_unpack.cc
    memory_bram.cc
    memory_map.cc
    memory_memx.cc
    memory_nordff.cc
    memory_narrow.cc
    memory_libmap.cc
    memory_bmux2rom.cc
    memlib.cc
)

set(YOSYS_PASSES_MEMORY_HEADERS
    memlib.h
)

add_library(Yosys::Passes::Memory OBJECT
    ${YOSYS_PASSES_MEMORY_SOURCES}
)

# expose the public headers for install
target_sources(Yosys::Passes::Memory
  FILE_SET HEADERS
    TYPE    HEADERS
    BASE_DIR ${CMAKE_CURRENT_SOURCE_DIR}
    FILES   ${YOSYS_PASSES_MEMORY_HEADERS}
)

target_link_libraries(Yosys::Passes::Memory
  PUBLIC
    Yosys::Interface
)

install(
  TARGETS Yosys::Passes::Memory
  FILE_SET HEADERS
    DESTINATION passes/memory
)
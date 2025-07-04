set(YOSYS_PASSES_FSM_SOURCES
    fsm.cc
    fsm_detect.cc
    fsm_extract.cc
    fsm_opt.cc
    fsm_expand.cc
    fsm_recode.cc
    fsm_info.cc
    fsm_export.cc
    fsm_map.cc
)

set(YOSYS_PASSES_FSM_HEADERS
    fsmdata.h
)

add_library(Yosys::Passes::Fsm OBJECT
    ${YOSYS_PASSES_FSM_SOURCES}
)

target_sources(Yosys::Passes::Fsm
  FILE_SET HEADERS
    TYPE    HEADERS
    BASE_DIR ${CMAKE_CURRENT_SOURCE_DIR}
    FILES   ${YOSYS_PASSES_FSM_HEADERS}
)

target_link_libraries(Yosys::Passes::Fsm
  PUBLIC
    Yosys::Interface
)

install(
  TARGETS Yosys::Passes::Fsm
  FILE_SET HEADERS      DESTINATION passes/fsm
)
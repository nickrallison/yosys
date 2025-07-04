set(YOSYS_PASSES_SAT_SOURCES
    sat.cc
    freduce.cc
    eval.cc
    miter.cc
    expose.cc
    assertpmux.cc
    clk2fflogic.cc
    async2sync.cc
    formalff.cc
    supercover.cc
    fmcombine.cc
    mutate.cc
    cutpoint.cc
    fminit.cc
    recover_names.cc
    synthprop.cc
)

if(ENABLE_ZLIB)
  list(APPEND YOSYS_PASSES_SAT_SOURCES
       sim.cc
  )
endif()

if(NOT DISABLE_SPAWN)
  list(APPEND YOSYS_PASSES_SAT_SOURCES
       qbfsat.cc
  )
endif()

add_library(Yosys::Passes::Sat OBJECT
  ${YOSYS_PASSES_SAT_SOURCES}
)

target_link_libraries(Yosys::Passes::Sat
  PUBLIC
    Yosys::Interface
)
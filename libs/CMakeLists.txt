set(YOSYS_LIBS_SOURCES
    bigint/BigInteger.cc
    bigint/BigIntegerAlgorithms.cc
    bigint/BigIntegerUtils.cc
    bigint/BigUnsigned.cc
    bigint/BigUnsignedInABase.cc

    sha1/sha1.cpp

    json11/json11.cpp

    ezsat/ezsat.cc
    ezsat/ezminisat.cc

    minisat/Options.cc
    minisat/SimpSolver.cc
    minisat/Solver.cc
    minisat/System.cc

    subcircuit/subcircuit.cc
)

set(YOSYS_LIBS_HEADERS
    bigint/BigInteger.hh
    bigint/BigIntegerAlgorithms.hh
    bigint/BigIntegerLibrary.hh
    bigint/BigIntegerUtils.hh
    bigint/BigUnsigned.hh
    bigint/BigUnsignedInABase.hh
    bigint/NumberlikeArray.hh

    sha1/sha1.h

    json11/json11.hpp

    ezsat/ezsat.h
    ezsat/ezminisat.h

    minisat/Alg.h
    minisat/Alloc.h
    minisat/Dimacs.h
    minisat/Heap.h
    minisat/IntMap.h
    minisat/IntTypes.h
    minisat/Map.h
    minisat/Options.h
    minisat/ParseUtils.h
    minisat/Queue.h
    minisat/Rnd.h
    minisat/SimpSolver.h
    minisat/Solver.h
    minisat/SolverTypes.h
    minisat/Sort.h
    minisat/System.h
    minisat/Vec.h
    minisat/XAlloc.h

    subcircuit/subcircuit.h

    cxxopts/include/cxxopts.hpp
)

if (ENABLE_ZLIB)
    list(APPEND YOSYS_LIBS_SOURCES
        fst/fastlz.cc
        fst/fstapi.cc
        fst/lz4.cc
    )
    list(APPEND YOSYS_LIBS_HEADERS
        fst/config.h
        fst/fastlz.h
        fst/fstapi.h
        fst/fst_win_unistd.h
        fst/lz4.h
    )
endif()

add_library(Yosys::Libs OBJECT
  ${YOSYS_LIBS_SOURCES}
)

target_sources(Yosys::Libs
  FILE_SET HEADERS
    TYPE    HEADERS
    BASE_DIR ${CMAKE_CURRENT_SOURCE_DIR}
    FILES   ${YOSYS_LIBS_HEADERS}
)

target_include_directories(Yosys::Libs
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
    $<INSTALL_INTERFACE:libs>
)

target_link_libraries(Yosys::Libs
  PUBLIC
    Yosys::Interface
)

install(
  TARGETS Yosys::Libs
  FILE_SET HEADERS      DESTINATION libs
)


add_library(yosys_libs OBJECT
    bigint/BigInteger.cc
    bigint/BigInteger.hh
    bigint/BigIntegerAlgorithms.cc
    bigint/BigIntegerAlgorithms.hh
    bigint/BigIntegerLibrary.hh
    bigint/BigIntegerUtils.cc
    bigint/BigIntegerUtils.hh
    bigint/BigUnsigned.cc
    bigint/BigUnsigned.hh
    bigint/BigUnsignedInABase.cc
    bigint/BigUnsignedInABase.hh
    bigint/NumberlikeArray.hh 

    sha1/sha1.cpp
    sha1/sha1.h

    json11/json11.cpp
    json11/json11.hpp

    ezsat/ezsat.cc
    ezsat/ezsat.h
    ezsat/ezminisat.cc
    ezsat/ezminisat.h

    minisat/Alg.h
    minisat/Alloc.h
    minisat/Dimacs.h
    minisat/Heap.h
    minisat/IntMap.h
    minisat/IntTypes.h
    minisat/Map.h
    minisat/Options.cc
    minisat/Options.h
    minisat/ParseUtils.h
    minisat/Queue.h
    minisat/Rnd.h
    minisat/SimpSolver.cc
    minisat/SimpSolver.h
    minisat/Solver.cc
    minisat/Solver.h
    minisat/SolverTypes.h
    minisat/Sort.h
    minisat/System.cc
    minisat/System.h
    minisat/Vec.h
    minisat/XAlloc.h
    
    cxxopts/include/cxxopts.hpp
)

target_sources(yosys_kernel 
    PRIVATE
        subcircuit/subcircuit.cc
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS
            ${CMAKE_CURRENT_SOURCE_DIR}/subcircuit
        FILES
            subcircuit/subcircuit.h

)

if (ENABLE_ZLIB)
target_sources(yosys_libs PRIVATE
    fst/config.h
    fst/fastlz.cc
    fst/fastlz.h
    fst/fstapi.cc
    fst/fstapi.h
    fst/fst_win_unistd.h
    fst/lz4.cc
    fst/lz4.h
)
endif()

target_link_libraries(yosys_obj PUBLIC yosys_libs)
target_sources(yosys_obj PUBLIC $<TARGET_OBJECTS:yosys_libs>)

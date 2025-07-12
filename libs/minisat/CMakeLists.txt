cmake_minimum_required(VERSION 3.23)
project(yosys_libs_minisat LANGUAGES CXX)


add_library(${PROJECT_NAME})
target_sources(
    ${PROJECT_NAME}
    PRIVATE
        Options.cc
        SimpSolver.cc
        Solver.cc
        System.cc

    PUBLIC
    FILE_SET HEADERS
    BASE_DIRS .
    FILES
        Alg.h
        Alloc.h
        Dimacs.h
        Heap.h
        IntMap.h
        IntTypes.h
        Map.h
        Options.h
        ParseUtils.h
        Queue.h
        Rnd.h
        SimpSolver.h
        Solver.h
        SolverTypes.h
        Sort.h
        System.h
        Vec.h
        XAlloc.h
)

target_include_directories(${PROJECT_NAME}
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
        $<INSTALL_INTERFACE:include>
)

add_library(minisat ALIAS ${PROJECT_NAME})
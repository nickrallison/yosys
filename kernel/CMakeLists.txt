cmake_minimum_required(VERSION 3.23)
project(yosys_kernel LANGUAGES CXX)

find_package(Git)
if(Git_FOUND)
    execute_process(
        COMMAND ${GIT_EXECUTABLE} rev-parse --short=9 HEAD
        WORKING_DIRECTORY ${yosys_SOURCE_DIR}
        OUTPUT_VARIABLE CURRENT_GIT_VERSION
        OUTPUT_STRIP_TRAILING_WHITESPACE
    )
    set(YOSYS_GIT_VERSION "git sha1 ${CURRENT_GIT_VERSION}, ")
endif()

configure_file(${CMAKE_CURRENT_SOURCE_DIR}/version.cc.in ${CMAKE_CURRENT_BINARY_DIR}/version.cc)
set_property(SOURCE log.cc APPEND PROPERTY COMPILE_DEFINITIONS YOSYS_SRC="${PROJECT_SOURCE_DIR}")

add_library(${PROJECT_NAME} STATIC)
target_sources(
    ${PROJECT_NAME}
    PRIVATE
        binding.cc
        calc.cc
        cellaigs.cc
        celledges.cc
        cost.cc
        drivertools.cc
        ff.cc
        ffmerge.cc
        fmt.cc
        functional.cc
        gzip.cc
        io.cc
        json.cc
        log.cc
        mem.cc
        qcsat.cc
        register.cc
        rtlil.cc
        satgen.cc
        scopeinfo.cc
        sexpr.cc
        tclapi.cc
        ${CMAKE_CURRENT_BINARY_DIR}/version.cc
        yosys.cc
        yw.cc

    PUBLIC
    FILE_SET HEADERS
    BASE_DIRS .
    FILES
        binding.h
        bitpattern.h
        cellaigs.h
        celledges.h
        celltypes.h
        compute_graph.h
        consteval.h
        cost.h
        drivertools.h
        ff.h
        ffinit.h
        ffmerge.h
        fmt.h
        functional.h
        gzip.h
        hashlib.h
        json.h
        log.h
        macc.h
        mem.h
        modtools.h
        qcsat.h
        register.h
        rtlil.h
        satgen.h
        scopeinfo.h
        sexpr.h
        sigtools.h
        timinginfo.h
        topo_scc.h
        utils.h
        yosys_common.h
        yosys.h
        yw.h

        ############
        constids.inc
)



if (ENABLE_ZLIB)
    find_package(ZLIB REQUIRED)
    add_compile_definitions(YOSYS_ENABLE_ZLIB)

    target_sources(
        ${PROJECT_NAME}
        PRIVATE
            fstdata.cc
        PUBLIC
        FILE_SET HEADERS
        BASE_DIRS .
        FILES
            fstdata.h
    )

    target_link_libraries(${PROJECT_NAME}
        PRIVATE 
            fst
            ${ZLIB_LIBRARIES}
    )
    target_include_directories(${PROJECT_NAME}
        PUBLIC
            ${ZLIB_INCLUDE_DIRS}
    )
    
endif()

target_link_libraries(${PROJECT_NAME}
    PRIVATE 
        bigint
        json11
        ezsat

        yosys_techlibs_common
        yosys_frontends_verilog
        yosys_backends_rtlil
)

target_include_directories(${PROJECT_NAME}
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}
        ${yosys_SOURCE_DIR}
)

if (ENABLE_READLINE)
    find_package(Readline REQUIRED)
    target_compile_definitions(${PROJECT_NAME} PUBLIC YOSYS_ENABLE_READLINE)
    target_link_libraries(${PROJECT_NAME} PUBLIC ${READLINE_LIBRARY})
    target_include_directories(${PROJECT_NAME} PUBLIC ${READLINE_INCLUDE_DIR})
endif()

if (ENABLE_EDITLINE)
    find_package(Editline REQUIRED)
    target_compile_definitions(${PROJECT_NAME} PUBLIC YOSYS_ENABLE_EDITLINE)
    target_link_libraries(${PROJECT_NAME} PUBLIC ${EDITLINE_LIBRARY})
    target_include_directories(${PROJECT_NAME} PUBLIC ${EDITLINE_INCLUDE_DIR})
endif()

if (ENABLE_COVER)
    target_compile_definitions(${PROJECT_NAME} PUBLIC YOSYS_ENABLE_COVER)
endif()

if (ENABLE_TCL)
    find_package(TCL 8.6 REQUIRED)
    target_compile_definitions(${PROJECT_NAME} PUBLIC YOSYS_ENABLE_TCL)
    target_include_directories(${PROJECT_NAME} PUBLIC ${TCL_INCLUDE_PATH})
    target_link_libraries(${PROJECT_NAME} PUBLIC ${TCL_LIBRARY})
endif()

target_compile_definitions(${PROJECT_NAME} PUBLIC
    _YOSYS_
)

# include(${yosys_SOURCE_DIR}/frontends/verilog/frontends_verilog.cmake)

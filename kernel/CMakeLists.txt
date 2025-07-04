
#if(CMAKE_PROJECT_VERSION_PATCH GREATER 0)
#    set(YOSYS_VERSION "${CMAKE_PROJECT_VERSION_MAJOR}.${CMAKE_PROJECT_VERSION_MINOR}+${CMAKE_PROJECT_VERSION_PATCH}")
#else()
#    set(YOSYS_VERSION "${CMAKE_PROJECT_VERSION_MAJOR}.${CMAKE_PROJECT_VERSION_MINOR}")
#endif()

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

set(YOSYS_KERNEL_SOURCES
    binding.cc
    calc.cc
    cellaigs.cc
    celledges.cc
    constids.inc
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
    yosys.cc
    yw.cc
    ${CMAKE_CURRENT_BINARY_DIR}/version.cc
)

set(YOSYS_KERNEL_HEADERS
    binding.h
    bitpattern.h
    cellaigs.h
    celledges.h
    celltypes.h
    compute_graph.h
    consteval.h
    constids.inc
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
)

if (ENABLE_ZLIB)
    list(APPEND YOSYS_KERNEL_SOURCES fstdata.cc)
    list(APPEND YOSYS_KERNEL_HEADERS fstdata.h)
endif()

add_library(Yosys::Kernel OBJECT
  ${YOSYS_KERNEL_SOURCES}
)

target_sources(Yosys::Kernel
  FILE_SET HEADERS
    TYPE    HEADERS
    BASE_DIR ${CMAKE_CURRENT_SOURCE_DIR}
    FILES   ${YOSYS_KERNEL_HEADERS}
)

target_include_directories(Yosys::Kernel
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
    $<INSTALL_INTERFACE:kernel>
)

target_link_libraries(Yosys::Kernel
  PUBLIC
    Yosys::Interface
)

install(
  TARGETS Yosys::Kernel
  FILE_SET HEADERS      DESTINATION kernel
)

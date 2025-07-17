

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

configure_file(${CMAKE_CURRENT_SOURCE_DIR}/cmake/version.cc.in ${CMAKE_CURRENT_BINARY_DIR}/version.cc)
set_property(SOURCE src/log.cc APPEND PROPERTY COMPILE_DEFINITIONS YOSYS_SRC="${PROJECT_SOURCE_DIR}")

add_library(yosys_kernel OBJECT)

target_sources(
    yosys_kernel
    PRIVATE
        src/binding.cc
        src/calc.cc
        src/cellaigs.cc
        src/celledges.cc
        src/cost.cc
        src/drivertools.cc
        src/ff.cc
        src/ffmerge.cc
        src/fmt.cc
        src/functional.cc
        src/gzip.cc
        src/io.cc
        src/json.cc
        src/log.cc
        src/mem.cc
        src/qcsat.cc
        src/register.cc
        src/rtlil.cc
        src/satgen.cc
        src/scopeinfo.cc
        src/sexpr.cc
        src/tclapi.cc
        ${CMAKE_CURRENT_BINARY_DIR}/version.cc
        src/yosys.cc
        src/yw.cc


    PUBLIC
    FILE_SET HEADERS
    FILES
        include/binding.h
        include/bitpattern.h
        include/cellaigs.h
        include/celledges.h
        include/celltypes.h
        include/compute_graph.h
        include/consteval.h
        include/cost.h
        include/drivertools.h
        include/ff.h
        include/ffinit.h
        include/ffmerge.h
        include/fmt.h
        include/functional.h
        include/gzip.h
        include/hashlib.h
        include/json.h
        include/log.h
        include/macc.h
        include/mem.h
        include/modtools.h
        include/qcsat.h
        include/register.h
        include/rtlil.h
        include/satgen.h
        include/scopeinfo.h
        include/sexpr.h
        include/sigtools.h
        include/timinginfo.h
        include/topo_scc.h
        include/utils.h
        include/yosys_common.h
        include/yosys.h
        include/yw.h

        ####
        constids.inc
)

if (ENABLE_ZLIB)
    target_sources(yosys_kernel 
        PRIVATE
            src/fstdata.cc
        PUBLIC
            FILE_SET HEADERS
            FILES
            include/fstdata.h
    )
endif()

add_dependencies(yosys_kernel yosys_techlib_common)

# Install headers using file sets (CMake 3.23+)
install(TARGETS yosys_kernel
        FILE_SET HEADERS
        DESTINATION include/yosys/kernel)

target_include_directories(yosys_kernel
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include/yosys/kernel>
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/src
)
target_link_libraries(yosys_obj PUBLIC yosys_kernel)
target_sources(yosys_obj PUBLIC $<TARGET_OBJECTS:yosys_kernel>)

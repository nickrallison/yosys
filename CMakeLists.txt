cmake_minimum_required(VERSION 3.20)

project(yosys-superbuild NONE) # Renamed for clarity

include(ExternalProject)

find_program(MAKE_EXECUTABLE make REQUIRED)

ExternalProject_Add(
    yosys_build
    SOURCE_DIR          ${CMAKE_CURRENT_SOURCE_DIR}
    # WORKING_DIRECTORY   ${CMAKE_CURRENT_SOURCE_DIR}
    CONFIGURE_COMMAND   ""
    BUILD_COMMAND       ${MAKE_EXECUTABLE} -C ${CMAKE_CURRENT_SOURCE_DIR} -j 32
    INSTALL_COMMAND     ""
    UPDATE_COMMAND      ""
    PATCH_COMMAND       ""
)
add_library(yosys INTERFACE)
add_dependencies(yosys yosys_build)
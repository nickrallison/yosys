add_library(yosys_techlibs_common STATIC)

add_custom_command(
    COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_CURRENT_BINARY_DIR}/techlibs/common
	COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/cellhelp.py ${CMAKE_CURRENT_SOURCE_DIR}/simlib.v > ${CMAKE_CURRENT_BINARY_DIR}/simlib_help.inc
	DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/cellhelp.py ${CMAKE_CURRENT_SOURCE_DIR}/simlib.v
	OUTPUT simlib_help.inc
	COMMENT "Generating techlibs/common/simlib_help.inc..."
)
add_custom_command(
    COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_CURRENT_BINARY_DIR}/techlibs/common
	COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/cellhelp.py ${CMAKE_CURRENT_SOURCE_DIR}/simcells.v > ${CMAKE_CURRENT_BINARY_DIR}/simcells_help.inc
	DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/cellhelp.py ${CMAKE_CURRENT_SOURCE_DIR}/simcells.v
	OUTPUT simcells_help.inc
	COMMENT "Generating techlibs/common/simcells_help.inc..."
)

add_custom_target(yosys_techlibs_common_gen DEPENDS
	${CMAKE_CURRENT_BINARY_DIR}/simlib_help.inc
	${CMAKE_CURRENT_BINARY_DIR}/simcells_help.inc
)

target_sources(yosys_techlibs_common PRIVATE
    synth.cc
    prep.cc
)
target_include_directories(yosys_techlibs_common PUBLIC
	$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
	$<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
)

target_link_libraries(yosys_techlibs_common
	PUBLIC
		yosys_kernel
)

if (ENABLE_ABC)
    target_compile_definitions(${PROJECT_NAME} PUBLIC YOSYS_ENABLE_ABC)
    if (LINK_ABC)
        target_compile_definitions(${PROJECT_NAME} PUBLIC YOSYS_LINK_ABC)
        target_link_libraries(${PROJECT_NAME} PUBLIC $<TARGET_FILE:libabc>)
        add_dependencies(${PROJECT_NAME} libabc)
    endif()        
endif()

add_dependencies(yosys_techlibs_common yosys_techlibs_common_gen)

add_share_file("share" "simlib.v")
add_share_file("share" "simcells.v")
add_share_file("share" "techmap.v")
add_share_file("share" "smtmap.v")
add_share_file("share" "pmux2mux.v")
add_share_file("share" "adff2dff.v")
add_share_file("share" "dff2ff.v")
add_share_file("share" "gate2lut.v")
add_share_file("share" "cmp2lut.v")
add_share_file("share" "cells.lib")
add_share_file("share" "mul2dsp.v")
add_share_file("share" "abc9_model.v")
add_share_file("share" "abc9_map.v")
add_share_file("share" "abc9_unmap.v")
add_share_file("share" "cmp2lcu.v")
add_share_file("share" "cmp2softlogic.v")
add_share_file("share/choices" "choices/kogge-stone.v")
add_share_file("share/choices" "choices/han-carlson.v")
add_share_file("share/choices" "choices/sklansky.v")
                                                                                           
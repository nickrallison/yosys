cmake_minimum_required(VERSION 3.23)
project(yosys_passes_pmgen LANGUAGES CXX)

add_library(${PROJECT_NAME})

function(pmgen_command  _name _path)
    set(CUSTOM_TARGET_NAME ${_name}_pm_gen)
    set(GENERATED_HEADER ${yosys_BINARY_DIR}/${_path}/${_name}_pm.h)
    add_custom_command(
        OUTPUT ${GENERATED_HEADER}
        COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/pmgen.py -o ${GENERATED_HEADER} -p ${_name} ${yosys_SOURCE_DIR}/${_path}/${_name}.pmg
        DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/pmgen.py ${yosys_SOURCE_DIR}/${_path}/${_name}.pmg
        COMMENT "Generating ${_path}/${_name}_pm.h..."
    )
    add_custom_target(${CUSTOM_TARGET_NAME} DEPENDS ${GENERATED_HEADER})
    add_dependencies(${PROJECT_NAME} ${CUSTOM_TARGET_NAME})
endfunction()

pmgen_command(test_pmgen passes/pmgen)
pmgen_command(ice40_dsp techlibs/ice40)
pmgen_command(ice40_wrapcarry techlibs/ice40)
pmgen_command(xilinx_dsp techlibs/xilinx)
pmgen_command(xilinx_dsp48a techlibs/xilinx)
pmgen_command(xilinx_dsp_CREG techlibs/xilinx)
pmgen_command(xilinx_dsp_cascade techlibs/xilinx)
pmgen_command(microchip_dsp techlibs/microchip)
pmgen_command(microchip_dsp_CREG techlibs/microchip)
pmgen_command(microchip_dsp_cascade techlibs/microchip)
pmgen_command(xilinx_srl techlibs/xilinx)

add_custom_command(
    OUTPUT ${yosys_BINARY_DIR}/passes/opt/peepopt_pm.h
    COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/pmgen.py -o ${yosys_BINARY_DIR}/passes/opt/peepopt_pm.h -p peepopt
        ${yosys_SOURCE_DIR}/passes/opt/peepopt_shiftmul_right.pmg
        ${yosys_SOURCE_DIR}/passes/opt/peepopt_shiftmul_left.pmg
        ${yosys_SOURCE_DIR}/passes/opt/peepopt_shiftadd.pmg
        ${yosys_SOURCE_DIR}/passes/opt/peepopt_muldiv.pmg
        ${yosys_SOURCE_DIR}/passes/opt/peepopt_muldiv_c.pmg
        ${yosys_SOURCE_DIR}/passes/opt/peepopt_formal_clockgateff.pmg
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/pmgen.py
        ${yosys_SOURCE_DIR}/passes/opt/peepopt_shiftmul_right.pmg
        ${yosys_SOURCE_DIR}/passes/opt/peepopt_shiftmul_left.pmg
        ${yosys_SOURCE_DIR}/passes/opt/peepopt_shiftadd.pmg
        ${yosys_SOURCE_DIR}/passes/opt/peepopt_muldiv.pmg
        ${yosys_SOURCE_DIR}/passes/opt/peepopt_muldiv_c.pmg
        ${yosys_SOURCE_DIR}/passes/opt/peepopt_formal_clockgateff.pmg
    COMMENT "Generating passes/pmgen/peepopt_pm.h..."
)
add_custom_target(peepopt_pm DEPENDS ${yosys_BINARY_DIR}/passes/opt/peepopt_pm.h)
add_dependencies(${PROJECT_NAME} peepopt_pm)

target_sources(${PROJECT_NAME} PRIVATE
    test_pmgen.cc
    ${yosys_SOURCE_DIR}/techlibs/ice40/ice40_dsp.cc
    ${yosys_SOURCE_DIR}/techlibs/ice40/ice40_wrapcarry.cc
    ${yosys_SOURCE_DIR}/techlibs/xilinx/xilinx_dsp.cc
    ${yosys_SOURCE_DIR}/techlibs/microchip/microchip_dsp.cc
    ${yosys_SOURCE_DIR}/passes/opt/peepopt.cc
    ${yosys_SOURCE_DIR}/techlibs/xilinx/xilinx_srl.cc
)

target_include_directories(${PROJECT_NAME}
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
        $<BUILD_INTERFACE:${yosys_SOURCE_DIR}>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
        $<BUILD_INTERFACE:${yosys_BINARY_DIR}>
        $<INSTALL_INTERFACE:include>
)

target_link_libraries(${PROJECT_NAME}
    PUBLIC
        yosys_kernel
)


# target_sources(yosys_passes_pmgen PUBLIC ${yosys_BINARY_DIR}/passes/pmgen/test_pmgen_pm.h)

# target_sources(yosys_passes_pmgen PUBLIC ${yosys_BINARY_DIR}/techlibs/ice40/ice40_dsp_pm.h)
# target_sources(yosys_passes_pmgen PUBLIC ${yosys_BINARY_DIR}/techlibs/ice40/ice40_wrapcarry_pm.h)

# target_sources(yosys_passes_pmgen PUBLIC ${yosys_BINARY_DIR}/techlibs/xilinx/xilinx_dsp_pm.h)
# target_sources(yosys_passes_pmgen PUBLIC ${yosys_BINARY_DIR}/techlibs/xilinx/xilinx_dsp48a_pm.h)
# target_sources(yosys_passes_pmgen PUBLIC ${yosys_BINARY_DIR}/techlibs/xilinx/xilinx_dsp_CREG_pm.h)
# target_sources(yosys_passes_pmgen PUBLIC ${yosys_BINARY_DIR}/techlibs/xilinx/xilinx_dsp_cascade_pm.h)

# target_sources(yosys_passes_pmgen PUBLIC ${yosys_BINARY_DIR}/techlibs/microchip/microchip_dsp_pm.h)
# target_sources(yosys_passes_pmgen PUBLIC ${yosys_BINARY_DIR}/techlibs/microchip/microchip_dsp_CREG_pm.h)
# target_sources(yosys_passes_pmgen PUBLIC ${yosys_BINARY_DIR}/techlibs/microchip/microchip_dsp_cascade_pm.h)

# target_sources(yosys_passes_pmgen PUBLIC ${yosys_BINARY_DIR}/passes/opt/peepopt_pm.h)

# target_sources(yosys_passes_pmgen PUBLIC ${yosys_BINARY_DIR}/techlibs/xilinx/xilinx_srl_pm.h)

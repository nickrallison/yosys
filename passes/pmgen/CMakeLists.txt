add_library(Yosys::Passes::Pmgen OBJECT
    test_pmgen.cc
    ${PROJECT_SOURCE_DIR}/techlibs/ice40/ice40_dsp.cc
    ${PROJECT_SOURCE_DIR}/techlibs/ice40/ice40_wrapcarry.cc
    ${PROJECT_SOURCE_DIR}/techlibs/xilinx/xilinx_dsp.cc
    ${PROJECT_SOURCE_DIR}/techlibs/microchip/microchip_dsp.cc
    ${PROJECT_SOURCE_DIR}/techlibs/xilinx/xilinx_srl.cc
    ${PROJECT_SOURCE_DIR}/passes/opt/peepopt.cc
)

set(YOSYS_PASSES_PMGEN_HEADERS)

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
    add_dependencies(Yosys::Passes::Pmgen ${CUSTOM_TARGET_NAME})
    list(APPEND YOSYS_PASSES_PMGEN_HEADERS ${GENERATED_HEADER})
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
add_dependencies(Yosys::Passes::Pmgen peepopt_pm)
list(APPEND YOSYS_PASSES_PMGEN_HEADERS ${yosys_BINARY_DIR}/passes/opt/peepopt_pm.h)

target_sources(Yosys::Passes::Pmgen
  FILE_SET HEADERS
    TYPE    HEADERS
    BASE_DIR ${CMAKE_CURRENT_SOURCE_DIR}
    FILES   ${YOSYS_PASSES_PMGEN_HEADERS}
)

target_link_libraries(Yosys::Passes::Pmgen PUBLIC Yosys::Interface)

install(
  TARGETS Yosys::Passes::Pmgen
  FILE_SET HEADERS DESTINATION passes/pmgen
)
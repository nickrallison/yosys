

add_library(yosys_backends_verilog INTERFACE
    verilog_backend.cc
)

target_include_directories(yosys_backends_verilog INTERFACE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
    $<INSTALL_INTERFACE:include/yosys/backends/verilog>
)

target_link_libraries(yosys_kernel INTERFACE yosys_backends_verilog)

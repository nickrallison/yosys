

add_library(yosys_backends_verilog STATIC
    verilog_backend.cc
)

target_include_directories(yosys_backends_verilog PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
    $<INSTALL_INTERFACE:include/yosys/backends/verilog>
)

target_link_libraries(yosys_obj PUBLIC yosys_backends_verilog)
target_link_libraries(yosys_backends_verilog PUBLIC yosys_kernel)

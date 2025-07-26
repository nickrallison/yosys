

add_library(yosys_backends_rtlil INTERFACE)

target_sources(yosys_backends_rtlil
        INTERFACE
            rtlil_backend.cc
        INTERFACE
            FILE_SET HEADERS
            FILES
            rtlil_backend.h
    )

target_include_directories(yosys_backends_rtlil
    INTERFACE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
        $<INSTALL_INTERFACE:include/yosys/backends/rtlil>
)
target_link_libraries(yosys_kernel INTERFACE yosys_backends_rtlil)
# target_link_libraries(yosys_backends_rtlil INTERFACE yosys_kernel)




add_library(yosys_backends_rtlil STATIC)

target_sources(yosys_backends_rtlil
        PRIVATE
            rtlil_backend.cc
        PUBLIC
            FILE_SET HEADERS
            FILES
            rtlil_backend.h
    )

target_include_directories(yosys_backends_rtlil
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
        $<INSTALL_INTERFACE:include/yosys/backends/rtlil>
)
target_link_libraries(yosys_obj PUBLIC yosys_backends_rtlil)
target_link_libraries(yosys_backends_rtlil PUBLIC yosys_kernel)


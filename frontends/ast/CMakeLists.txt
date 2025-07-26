

add_library(yosys_frontends_ast INTERFACE)

target_sources(yosys_frontends_ast
        INTERFACE
            ast_binding.cc
            ast.cc
            dpicall.cc
            genrtlil.cc
            simplify.cc
        INTERFACE
            FILE_SET HEADERS
            FILES
                ast_binding.h
                ast.h
    )

target_include_directories(yosys_frontends_ast INTERFACE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
    $<INSTALL_INTERFACE:include/yosys/frontends/ast>
)

if (ENABLE_PLUGINS)
    target_include_directories(yosys_frontends_ast INTERFACE ${LIBFFI_INCLUDE_DIR})
    target_link_libraries(yosys_frontends_ast INTERFACE ${LIBFFI_LIBRARY})
endif()

# target_link_libraries(yosys_frontends_ast 
#     INTERFACE 
#         # yosys_frontends_rtlil 
#         # yosys_frontends_rtlil_gen
#         yosys_frontends_verilog

#         # yosys_backends_rtlil

#         yosys_passes_cmds
# )

target_link_libraries(yosys_kernel INTERFACE yosys_frontends_ast)
# target_link_libraries(yosys_frontends_ast PUBLIC yosys_kernel)

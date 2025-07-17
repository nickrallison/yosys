

add_library(yosys_frontends_ast STATIC)

target_sources(yosys_frontends_ast
        PRIVATE
            ast_binding.cc
            ast.cc
            dpicall.cc
            genrtlil.cc
            simplify.cc
        PUBLIC
            FILE_SET HEADERS
            FILES
                ast_binding.h
                ast.h
    )

target_include_directories(yosys_frontends_ast PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
    $<INSTALL_INTERFACE:include/yosys/frontends/ast>
)

if (ENABLE_PLUGINS)
    target_include_directories(yosys_frontends_ast PUBLIC ${LIBFFI_INCLUDE_DIR})
    target_link_libraries(yosys_frontends_ast PUBLIC ${LIBFFI_LIBRARY})
endif()

target_link_libraries(yosys_frontends_ast 
    PRIVATE yosys_passes_cmds
)

target_link_libraries(yosys_obj PUBLIC yosys_frontends_ast)
target_link_libraries(yosys_frontends_ast PUBLIC yosys_kernel)

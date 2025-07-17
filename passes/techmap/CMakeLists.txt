

add_library(yosys_passes_techmap OBJECT
    flatten.cc
    techmap.cc
    simplemap.cc
    dfflibmap.cc
    maccmap.cc
    booth.cc
    libcache.cc
    libparse.cc
    iopadmap.cc
    clkbufmap.cc
    hilomap.cc
    extract.cc
    extract_fa.cc
    extract_counter.cc
    extract_reduce.cc
    alumacc.cc
    dffinit.cc
    pmuxtree.cc
    bmuxmap.cc
    demuxmap.cc
    bwmuxmap.cc
    muxcover.cc
    aigmap.cc
    tribuf.cc
    lut2mux.cc
    nlutmap.cc
    shregmap.cc
    deminout.cc
    insbuf.cc
    bufnorm.cc
    attrmvcp.cc
    attrmap.cc
    zinit.cc
    dfflegalize.cc
    dffunmap.cc
    flowmap.cc
    extractinv.cc
    cellmatch.cc
    clockgate.cc
    constmap.cc
)

if (ENABLE_ABC)
    target_sources(yosys_passes_techmap PRIVATE
        abc.cc
        abc9.cc
        abc9_exe.cc
        abc9_ops.cc
        abc_new.cc
    )
endif()

target_link_libraries(yosys_obj PUBLIC yosys_passes_techmap)
target_link_libraries(yosys_passes_techmap PUBLIC yosys_kernel)

target_include_directories(yosys_passes_techmap
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
        # $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include/yosys/passes/techmap>
    # PRIVATE
    #     ${CMAKE_CURRENT_SOURCE_DIR}/src
)

target_sources(yosys_obj PUBLIC $<TARGET_OBJECTS:yosys_passes_techmap>)

if (NOT DISABLE_SPAWN)
    set(EXECUTABLE_OUTPUT_PATH ${PROJECT_BINARY_DIR})
    add_executable(yosys-filterlib filterlib.cc
        $<TARGET_OBJECTS:yosys_kernel>)
    target_link_libraries(yosys-filterlib PUBLIC yosys_kernel)
    install(TARGETS yosys-filterlib
            RUNTIME DESTINATION .)
endif()

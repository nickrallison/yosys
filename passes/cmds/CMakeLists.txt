cmake_minimum_required(VERSION 3.23)
project(yosys_passes_cmds LANGUAGES CXX)

add_library(${PROJECT_NAME})

target_sources(${PROJECT_NAME} PRIVATE
    add.cc
    delete.cc
    design.cc
    select.cc
    show.cc
    viz.cc
    rename.cc
    autoname.cc
    connect.cc
    scatter.cc
    setundef.cc
    splitnets.cc
    splitcells.cc
    stat.cc
    internal_stats.cc
    setattr.cc
    copy.cc
    splice.cc
    scc.cc
    glift.cc
    torder.cc
    logcmd.cc
    tee.cc
    write_file.cc
    connwrappers.cc
    cover.cc
    trace.cc
    plugin.cc
    check.cc
    edgetypes.cc
    portlist.cc
    chformal.cc
    chtype.cc
    blackbox.cc
    ltp.cc
    scratchpad.cc
    logger.cc
    printattrs.cc
    sta.cc
    clean_zerowidth.cc
    xprop.cc
    dft_tag.cc
    future.cc
    box_derive.cc
    example_dt.cc
    portarcs.cc
    wrapcell.cc
    setenv.cc
    test_select.cc
    abstract.cc
)

if (NOT DISABLE_SPAWN)
    target_sources(${PROJECT_NAME} PRIVATE
        exec.cc
        bugpoint.cc
    )
endif()

target_link_libraries(${PROJECT_NAME}
    PUBLIC
        yosys_kernel
)

target_include_directories(${PROJECT_NAME}
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
        $<BUILD_INTERFACE:${yosys_SOURCE_DIR}>
        $<INSTALL_INTERFACE:include>
)

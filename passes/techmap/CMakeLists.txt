add_library(Yosys::Passes::Techmap OBJECT
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

if(ENABLE_ABC)
    target_sources(Yosys::Passes::Techmap PRIVATE
        abc.cc
        abc9.cc
        abc9_exe.cc
        abc9_ops.cc
        abc_new.cc
    )
endif()

target_link_libraries(Yosys::Passes::Techmap
    PUBLIC
        Yosys::Interface
)

if(NOT DISABLE_SPAWN)
    add_executable(yosys-filterlib filterlib.cc)
    target_link_libraries(yosys-filterlib
        PUBLIC
            Yosys::Interface
    )
endif()
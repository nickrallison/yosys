cmake_minimum_required(VERSION 3.23)
project(yosys_passes_techmap LANGUAGES CXX)

add_library(${PROJECT_NAME})

target_sources(
    ${PROJECT_NAME}
    PRIVATE
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
    PUBLIC
    FILE_SET HEADERS
    BASE_DIRS .
    FILES
        libparse.h
        simplemap.h
)

if (ENABLE_ABC)
    target_sources(${PROJECT_NAME} PRIVATE
        abc.cc
        abc9.cc
        abc9_exe.cc
        abc9_ops.cc
        abc_new.cc
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
)

if (ENABLE_ABC)
    target_compile_definitions(${PROJECT_NAME} PUBLIC YOSYS_ENABLE_ABC)
    if (LINK_ABC)
        target_compile_definitions(${PROJECT_NAME} PUBLIC YOSYS_LINK_ABC)
        target_link_libraries(${PROJECT_NAME} PUBLIC $<TARGET_FILE:libabc>)
        add_dependencies(${PROJECT_NAME} libabc)
    endif()        
endif()

if (NOT DISABLE_SPAWN)
    set(EXECUTABLE_OUTPUT_PATH ${PROJECT_BINARY_DIR})
    add_executable(yosys-filterlib filterlib.cc)
    target_include_directories(yosys-filterlib
        PRIVATE
            ${CMAKE_CURRENT_SOURCE_DIR}
            ${yosys_SOURCE_DIR}
    )
    target_link_libraries(yosys-filterlib
        PRIVATE
            yosys_kernel
    )
endif()



add_library(yosys_backends_aiger OBJECT
    aiger.cc
    xaiger.cc
)

target_link_libraries(yosys_obj PUBLIC yosys_backends_aiger)
target_link_libraries(yosys_backends_aiger PUBLIC yosys_kernel)
target_sources(yosys_obj PUBLIC $<TARGET_OBJECTS:yosys_backends_aiger>)
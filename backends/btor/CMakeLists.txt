

add_library(yosys_backends_btor OBJECT
    btor.cc
)

target_link_libraries(yosys_obj PUBLIC yosys_backends_btor)
target_link_libraries(yosys_backends_btor PUBLIC yosys_kernel)
target_sources(yosys_obj PUBLIC $<TARGET_OBJECTS:yosys_backends_btor>)

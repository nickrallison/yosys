add_library(Yosys::Passes::Hierarchy OBJECT
    hierarchy.cc
    uniquify.cc
    submod.cc
    keep_hierarchy.cc
)

target_link_libraries(Yosys::Passes::Hierarchy
    PUBLIC
        Yosys::Interface
)
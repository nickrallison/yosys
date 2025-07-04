set(YOSYS_FRONTENDS_AIGER2_SOURCES
    xaiger.cc
)

add_library(Yosys::Frontends::Aiger2 OBJECT
    ${YOSYS_FRONTENDS_AIGER2_SOURCES}
)

target_link_libraries(Yosys::Frontends::Aiger2
    PUBLIC
        Yosys::Interface
)
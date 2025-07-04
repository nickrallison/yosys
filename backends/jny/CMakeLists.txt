add_library(Yosys::Backends::Jny OBJECT
    jny.cc
)

target_link_libraries(Yosys::Backends::Jny
    PUBLIC
        Yosys::Interface
)
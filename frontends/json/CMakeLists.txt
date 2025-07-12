add_library(yosys_frontends_json)

target_sources(yosys_frontends_json PRIVATE
    jsonparse.cc
)


target_link_libraries(yosys_frontends_json
    PRIVATE
        yosys_kernel
)

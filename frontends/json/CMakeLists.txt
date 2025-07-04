set(YOSYS_FRONTENDS_JSON_SOURCES
    jsonparse.cc
)

add_library(Yosys::Frontends::Json OBJECT
  ${YOSYS_FRONTENDS_JSON_SOURCES}
)

target_link_libraries(Yosys::Frontends::Json PUBLIC Yosys::Interface)
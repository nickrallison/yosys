set(YOSYS_FRONTENDS_LIBERTY_SOURCES
    liberty.cc
)

add_library(Yosys::Frontends::Liberty OBJECT
  ${YOSYS_FRONTENDS_LIBERTY_SOURCES}
)


target_link_libraries(Yosys::Frontends::Liberty PUBLIC Yosys::Interface)
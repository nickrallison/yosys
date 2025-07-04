set(YOSYS_FRONTENDS_VERIFIC_SOURCES
    verific.cc
    #verificsva.cc
)

add_library(Yosys::Frontends::Verific OBJECT
    ${YOSYS_FRONTENDS_VERIFIC_SOURCES})


target_link_libraries(Yosys::Frontends::Verific
  PUBLIC
    Yosys::Interface
)

set(YOSYS_FRONTENDS_RPC_SOURCES
    rpc_frontend.cc
)

add_library(Yosys::Frontends::Rpc OBJECT EXCLUDE_FROM_ALL
  ${YOSYS_FRONTENDS_RPC_SOURCES}
)

target_link_libraries(Yosys::Frontends::Rpc PUBLIC Yosys::Interface)

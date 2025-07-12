cmake_minimum_required(VERSION 3.23)
project(yosys_backends_rtlil LANGUAGES CXX)

add_library(${PROJECT_NAME})

target_sources(${PROJECT_NAME} PRIVATE
    rtlil_backend.cc
    rtlil_backend.h
)

target_sources(
    ${PROJECT_NAME}
    PRIVATE
        rtlil_backend.cc
    PUBLIC
    FILE_SET HEADERS
    BASE_DIRS .
    FILES
        rtlil_backend.h
)

target_link_libraries(${PROJECT_NAME}
    PUBLIC
        yosys_kernel
)

target_include_directories(${PROJECT_NAME}
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
        $<INSTALL_INTERFACE:include>
)
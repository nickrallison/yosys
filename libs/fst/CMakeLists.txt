cmake_minimum_required(VERSION 3.23)
project(yosys_libs_fst LANGUAGES CXX)

add_library(${PROJECT_NAME})
target_sources(
    ${PROJECT_NAME}
    PRIVATE
        fastlz.cc
        fstapi.cc
        lz4.cc

    PUBLIC
    FILE_SET HEADERS
    BASE_DIRS .
    FILES
        config.h
        fastlz.h
        fstapi.h
        fst_win_unistd.h
        lz4.h
)

target_include_directories(${PROJECT_NAME}
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
        $<INSTALL_INTERFACE:include>
)

target_link_libraries(${PROJECT_NAME} PUBLIC ZLIB::ZLIB)

add_library(fst ALIAS ${PROJECT_NAME})
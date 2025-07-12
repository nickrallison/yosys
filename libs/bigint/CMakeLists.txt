cmake_minimum_required(VERSION 3.23)
project(yosys_libs_bigint LANGUAGES CXX C)

add_library(${PROJECT_NAME})
target_sources(
    ${PROJECT_NAME}
    PRIVATE
        BigInteger.cc
        BigIntegerAlgorithms.cc
        BigIntegerUtils.cc
        BigUnsigned.cc
        BigUnsignedInABase.cc

    PUBLIC
    FILE_SET HEADERS
    BASE_DIRS .
    FILES
        BigInteger.hh
        BigIntegerAlgorithms.hh
        BigIntegerLibrary.hh
        BigIntegerUtils.hh
        BigUnsigned.hh
        BigUnsignedInABase.hh
        NumberlikeArray.hh
)

target_include_directories(${PROJECT_NAME}
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
        $<INSTALL_INTERFACE:include>
)

add_library(bigint ALIAS ${PROJECT_NAME})
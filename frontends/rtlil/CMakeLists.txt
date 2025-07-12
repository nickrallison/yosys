cmake_minimum_required(VERSION 3.23)
project(yosys_frontends_rtlil LANGUAGES CXX)

flex_target(RTLIL_LEXER "rtlil_lexer.l" "${CMAKE_CURRENT_BINARY_DIR}/rtlil_lexer.cc")
bison_target(RTLIL_PARSER "rtlil_parser.y" "${CMAKE_CURRENT_BINARY_DIR}/rtlil_parser.tab.cc" DEFINES_FILE "${CMAKE_CURRENT_BINARY_DIR}/rtlil_parser.tab.hh" COMPILE_FLAGS "-d -r all")

add_library(${PROJECT_NAME})
target_sources(
    ${PROJECT_NAME}
    PRIVATE
        rtlil_frontend.cc
    PUBLIC
    FILE_SET HEADERS
    BASE_DIRS .
    FILES
        rtlil_frontend.h
)

target_link_libraries(${PROJECT_NAME}
    PUBLIC
        yosys_kernel
)

add_library(${PROJECT_NAME}_gen OBJECT
    ${FLEX_RTLIL_LEXER_OUTPUTS}
    ${BISON_RTLIL_PARSER_OUTPUTS}
)

target_include_directories(${PROJECT_NAME}
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
        $<INSTALL_INTERFACE:include>
)

target_link_libraries(${PROJECT_NAME}_gen PUBLIC yosys_kernel)
target_link_libraries(${PROJECT_NAME} PUBLIC ${PROJECT_NAME}_gen)
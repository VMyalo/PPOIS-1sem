# CMakeLists.txt
cmake_minimum_required(VERSION 3.15)
project(LongIntegerTests LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Поиск UnitTest++ через vcpkg
find_path(UNITTEST++_INCLUDE_DIR
    NAMES UnitTest++/UnitTest++.h
    REQUIRED
)
find_library(UNITTEST++_LIBRARY
    NAMES UnitTest++
    REQUIRED
)

# Исходники
set(SOURCES
    src/long_integer.cpp
    tests/test_long_integer.cpp
)

# Исполняемый файл тестов
add_executable(test_long_integer ${SOURCES})

# Подключаем заголовки и библиотеку
target_include_directories(test_long_integer PRIVATE
    include
    ${UNITTEST++_INCLUDE_DIR}
)

target_link_libraries(test_long_integer PRIVATE
    ${UNITTEST++_LIBRARY}
)

# Включаем предупреждения
target_compile_options(test_long_integer PRIVATE
    -Wall -Wextra -Wpedantic
)

# Автоматически добавляем флаги для coverage, если:
# - сборка в Debug
# - компилятор — GCC
if(CMAKE_BUILD_TYPE STREQUAL "Debug" AND CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    target_compile_options(test_long_integer PRIVATE
        -fprofile-arcs -ftest-coverage
    )
    target_link_options(test_long_integer PRIVATE
        -fprofile-arcs -ftest-coverage
    )
    message(STATUS "Enabled code coverage (GCC + Debug)")
endif()
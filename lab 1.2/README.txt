# Сконфигурировать
cmake .. \
    -DCMAKE_BUILD_TYPE=Debug \
    -DCMAKE_TOOLCHAIN_FILE=/path/to/vcpkg/scripts/buildsystems/vcpkg.cmake

# Собрать
cmake --build .

# Запустить тесты
./test_long_integer

# Генерация отчёта
gcovr \
    -r . \
    --filter 'src/' \
    --filter 'include/' \
    --exclude 'tests/' \
    --txt \
    --html-details build/coverage/index.html \
    --print-summary
cmake_minimum_required(VERSION 3.10)
project(quark)

find_package(CUDA REQUIRED)

add_subdirectory(Catzilla)
add_subdirectory(plugins)


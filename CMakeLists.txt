cmake_minimum_required(VERSION 3.14)
project(quark-plugins)

find_package(CUDA REQUIRED)

add_subdirectory(Catzilla)
add_subdirectory(plugins)


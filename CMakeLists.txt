cmake_minimum_required(VERSION 3.13)
set(CMAKE_POLICY_VERSION_MINIMUM 3.5)
project(quark-plugins)

# 启用 FetchContent
include(FetchContent)

# 定义 msgpack-c 的 Git 仓库
FetchContent_Declare(
    msgpack
    GIT_REPOSITORY git@github.com:msgpack/msgpack-c.git
    GIT_TAG        cpp-6.0.0  # 使用特定版本
)

# 下载并配置 msgpack-c
FetchContent_MakeAvailable(msgpack)

find_package(CUDA REQUIRED)

add_subdirectory(Catzilla)
add_subdirectory(plugins)


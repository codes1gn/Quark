file(GLOB PLUGINS_SOURCES
  src/plugins.cpp
  src/options.cpp
  src/arguments.cpp
)

add_library(plugins STATIC ${PLUGINS_SOURCES})

# TODO: make it configurable, read and iterate from config
target_include_directories(plugins PUBLIC
  ${CMAKE_CURRENT_SOURCE_DIR}/include
  ${CMAKE_CURRENT_SOURCE_DIR}/../Catzilla
)
target_include_directories(plugins PRIVATE ${msgpack_SOURCE_DIR}/include)

# TODO: make it auto
target_link_libraries(plugins PRIVATE
  catz
  catz-recipes-lib
  msgpack-cxx
)

# plugin execute
add_executable(quark-plugins src/cli.cpp)
target_link_libraries(quark-plugins PRIVATE plugins)


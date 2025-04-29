file(GLOB PLUGINS_SOURCES
  src/*.cpp
)

add_library(plugins STATIC ${PLUGINS_SOURCES})

# TODO: make it configurable, read and iterate from config
target_include_directories(plugins PUBLIC
  ${CMAKE_CURRENT_SOURCE_DIR}/include
  ${CMAKE_CURRENT_SOURCE_DIR}/../Catzilla
)

# TODO: make it auto
target_link_libraries(plugins PRIVATE
  catz
  catz-recipes-lib
)

# plugin execute
add_executable(quark-plugins-exec src/cli.cpp)
target_link_libraries(quark-plugins-exec PRIVATE plugins)

#ifndef SERIALISATION_H
#define SERIALISATION_H

#include <msgpack.hpp>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>

template <typename T>
void serialize_to_file(const T& data, const std::string& filename) {
  msgpack::sbuffer buffer;
  msgpack::pack(buffer, data);

  std::ofstream ofs(filename, std::ios::binary);
  ofs.write(buffer.data(), buffer.size());
}

template <typename T>
T deserialize(const std::string& filename) {
  std::ifstream ifs(filename, std::ios::binary);
  if (!ifs) {
      throw std::runtime_error("Failed to open file: " + filename);
  }

  std::stringstream buffer;
  buffer << ifs.rdbuf();
  std::string data = buffer.str();

  msgpack::object_handle oh = msgpack::unpack(data.data(), data.size());
  msgpack::object obj = oh.get();

  T result;
  obj.convert(result);

  return result;
}

#endif // SERIALISATION_H

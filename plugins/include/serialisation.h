#ifndef SERIALISATION_H
#define SERIALISATION_H

#include <msgpack.hpp>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>

// SER/DESER structural data to msgpack, (e.g. vector<vector<float>>)
template <typename T>
void serialiseToMsgpack(const T& data, const std::string& filename) {
  msgpack::sbuffer buffer;
  msgpack::pack(buffer, data);

  std::ofstream ofs(filename, std::ios::binary);
  ofs.write(buffer.data(), buffer.size());
}

template <typename T>
T deserialiseFromMsgpack(const std::string& filename) {
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

// SER/DESER float* to msgpack, (e.g. float*)
// TODO: generalise to T*
template <typename T>
T* deserialisePtrFromMsgpack(const std::string& file_path) {
    std::ifstream file(file_path, std::ios::binary);
    if (!file) {
        throw std::runtime_error("Failed to open file");
    }

    file.seekg(0, std::ios::end);
    int size = file.tellg() / sizeof(T);  // 计算元素数量
    file.seekg(0, std::ios::beg);

    T* data = new T[size];

    file.read(reinterpret_cast<char*>(data), size * sizeof(T));
    file.close();

    return data;
}
// NOTE: C++ T* does not have size info, we need extra arg here.
// however, we can consider to use msgpack filesize, to infer, but this API
// should only update the data content, thus, we make it explicit below
template <typename T>
void serialisePtrToMsgpack(const std::string& file_path, T* data, int size) {
    std::ofstream file(file_path, std::ios::binary);
    if (!file) {
        throw std::runtime_error("Failed to open file");
    }

    // 创建 msgpack::sbuffer 对象
    msgpack::sbuffer buffer;

    // 将数据打包到 buffer 中
    msgpack::pack(buffer, std::vector<T>(data, data + size));

    // 将 buffer 写入文件
    file.write(buffer.data(), buffer.size());
    file.close();
}

template <typename T>
void updatePtrToMsgpack(const std::string& file_path, T* data, size_t size) {
    std::ofstream file(file_path, std::ios::binary);
    if (!file) {
        throw std::runtime_error("Failed to open file");
    }

    // 创建 msgpack::sbuffer 对象
    msgpack::sbuffer buffer;

    // 将数据打包到 buffer 中
    msgpack::pack(buffer, std::vector<T>(data, data + size));

    // 将 buffer 写入文件
    file.write(buffer.data(), buffer.size());
    file.close();
}

#endif // SERIALISATION_H

// plugins/src/plugins.cpp
#include "plugins.h"
#include <iostream>
#include <stdexcept>

#include "recipes/recipes.h"
#include "serialisation.h"
// TODO: strong arguments function

namespace quark {

void Plugins::smoke_test() {
  std::cout << "Smoke test passed! Plugins::smoke_test called successfully." << std::endl;
}

bool Plugins::execute(const std::string &executor, const std::string &opkind, const std::vector<std::string> &arguments) { 
  if (executor == "test" && opkind == "test") {
    std::cout << "hello\n";
    std::cout << arguments[0] << std::endl;
    auto data = deserialiseFromMsgpack<std::vector<std::vector<float>>>(arguments[0]);
    std::cout << "Loaded data size: " << data.size() << std::endl;
    for (const auto& row : data) {
        std::cout << "Row size: " << row.size() << std::endl;
    }

    std::cout << "C++: Processing data:" << std::endl;
    for (const auto& row : data) {
        for (float val : row) {
            std::cout << val << " ";
        }
        std::cout << std::endl;
    }

    return true;
  }
  if (executor == "catzilla") {
    if (opkind == "matmul") {
      for (const auto &str : arguments) {
        std::cout << str << " ";
      }
      std::cout << std::endl;
      if (arguments.size() < 8) {
        throw std::invalid_argument("matmul requires 8 arguments: M N K alpha A B beta C");
      }

      int M = std::stoi(arguments[0]);
      int N = std::stoi(arguments[1]);
      int K = std::stoi(arguments[2]);
      float alpha = std::stof(arguments[3]);
      // auto A = deserialize<std::vector<std::vector<float>>>(arguments[4]);
      // auto B = deserialize<std::vector<std::vector<float>>>(arguments[5]);
      // auto C = deserialize<std::vector<std::vector<float>>>(arguments[7]);
      float* A = deserialisePtrFromMsgpack<float>(arguments[4]);
      float* B = deserialisePtrFromMsgpack<float>(arguments[5]);
      float* C = deserialisePtrFromMsgpack<float>(arguments[7]);
      std::cout << "Matrix A:" << std::endl;
      for (int i = 0; i < 4; ++i) {
          for (int j = 0; j < 4; ++j) {
              std::cout << A[i * 64 + j] << " ";
          }
          std::cout << std::endl;
      }

      std::cout << "Matrix B:" << std::endl;
      for (int i = 0; i < 4; ++i) {
          for (int j = 0; j < 4; ++j) {
              std::cout << B[i * 64 + j] << " ";
          }
          std::cout << std::endl;
      }
      float beta = std::stof(arguments[6]);

      catz::recipes::matmul(M, N, K, alpha, A, B, beta, C);
      updatePtrToMsgpack<float>(arguments[7], C, M*N);
      std::cout << "Matrix multiplication completed by catzilla." << std::endl;
    } else {
      return false;
    }
  }
  return true;
}

} // namespace quark

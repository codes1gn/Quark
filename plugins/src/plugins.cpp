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
    std::string filename = "quark_data.msgpack";
    auto data = deserialize<std::vector<std::vector<float>>>(filename);
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
      float *A = reinterpret_cast<float *>(std::stoull(arguments[4], nullptr, 0));
      float *B = reinterpret_cast<float *>(std::stoull(arguments[5], nullptr, 0));
      std::cout << A[0] << std::endl;
      // std::cout << "Matrix A:" << std::endl;
      // for (int i = 0; i < 4; ++i) {
      //     for (int j = 0; j < 4; ++j) {
      //         std::cout << A[i * 64 + j] << " ";
      //     }
      //     std::cout << std::endl;
      // }
      // std::cout << std::flush;
      //
      // std::cout << "Matrix B:" << std::endl;
      // for (int i = 0; i < 4; ++i) {
      //     for (int j = 0; j < 4; ++j) {
      //         std::cout << B[i * 64 + j] << " ";
      //     }
      //     std::cout << std::endl;
      // }
      // std::cout << std::flush;
      float beta = std::stof(arguments[6]);
      float *C = reinterpret_cast<float *>(std::stoull(arguments[7], nullptr, 0));

      catz::recipes::matmul(M, N, K, alpha, A, B, beta, C);
      std::cout << "Matrix multiplication completed by catzilla." << std::endl;
    } else {
      return false;
    }
  }
  return true;
}

} // namespace quark

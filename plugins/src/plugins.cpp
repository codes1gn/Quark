// plugins/src/plugins.cpp
#include "plugins.h"
#include <iostream>
#include <stdexcept>

#include "recipes/recipes.h"
// TODO: strong arguments function

namespace quark {

void Plugins::smoke_test() {
    std::cout << "Smoke test passed! Plugins::smoke_test called successfully." << std::endl;
}

void Plugins::execute(const std::string &executor, const std::string &opkind, const std::vector<std::string> &arguments) { if (executor == "catzilla") {
    if (opkind == "matmul") {
      if (arguments.size() < 8) {
        throw std::invalid_argument("matmul requires 8 arguments: M N K alpha A B beta C");
      }

      int M = std::stoi(arguments[0]);
      int N = std::stoi(arguments[1]);
      int K = std::stoi(arguments[2]);
      float alpha = std::stof(arguments[3]);
      float *A = reinterpret_cast<float *>(std::stol(arguments[4]));  // 假设 A 是内存地址
      float *B = reinterpret_cast<float *>(std::stol(arguments[5]));  // 假设 B 是内存地址
      float beta = std::stof(arguments[6]);
      float *C = reinterpret_cast<float *>(std::stol(arguments[7]));  // 假设 C 是内存地址

      catz::recipes::matmul(M, N, K, alpha, A, B, beta, C);
      std::cout << "Matrix multiplication completed by catzilla." << std::endl;
    } else {
      throw std::invalid_argument("Unknown operator: " + opkind);
    }
  } else {
    throw std::invalid_argument("Unknown executor: " + executor);
  }
}

} // namespace quark

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

bool Plugins::execute(const std::string &executor, const std::string &opkind, const std::vector<std::string> &arguments) { 
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
      float *A = reinterpret_cast<float *>(std::stoul(arguments[4], nullptr, 16));
      float *B = reinterpret_cast<float *>(std::stoul(arguments[5], nullptr, 16));
      float beta = std::stof(arguments[6]);
      float *C = reinterpret_cast<float *>(std::stoul(arguments[7], nullptr, 16));

      catz::recipes::matmul(M, N, K, alpha, A, B, beta, C);
      std::cout << "Matrix multiplication completed by catzilla." << std::endl;
    } else {
      return false;
    }
  } else {
    return false;
  }
  return true;
}

} // namespace quark

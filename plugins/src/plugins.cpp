// plugins/src/plugins.cpp
#include <iostream>
#include <stdexcept>

#include "arguments.h"
#include "plugins.h"
#include "recipes/recipes.h"
#include "serialisation.h"
// TODO: strong arguments function

namespace quark {

namespace {

void matmul_wrapper(const std::vector<OperatorArg> &args) {
  int M = std::get<int>(args[0]);
  int N = std::get<int>(args[1]);
  int K = std::get<int>(args[2]);
  float alpha = std::get<float>(args[3]);
  float *A = std::get<float *>(args[4]);
  float *B = std::get<float *>(args[5]);
  float beta = std::get<float>(args[6]);
  float *C = std::get<float *>(args[7]);

  catz::recipes::matmul(M, N, K, alpha, A, B, beta, C);

  std::cout << "Matrix multiplication executed with M=" << M << ", N=" << N
            << ", K=" << K << std::endl;
}

} // namespace

void Plugins::smoke_test() {
  std::cout << "Smoke test passed! Plugins::smoke_test called successfully."
            << std::endl;
}

bool Plugins::execute(const std::string &executor, const std::string &opkind,
                      const std::vector<std::string> &arguments) {
  if (executor == "test" && opkind == "test") {
    std::cout << "hello\n";
    std::cout << arguments[0] << std::endl;
    auto data =
        deserialiseFromMsgpack<std::vector<std::vector<float>>>(arguments[0]);
    std::cout << "Loaded data size: " << data.size() << std::endl;
    for (const auto &row : data) {
      std::cout << "Row size: " << row.size() << std::endl;
    }

    std::cout << "C++: Processing data:" << std::endl;
    for (const auto &row : data) {
      for (float val : row) {
        std::cout << val << " ";
      }
      std::cout << std::endl;
    }

    return true;
  }
  if (executor == "catzilla") {
    if (opkind == "matmul") {
      std::vector<std::string> expected_types = {
          "int", "int", "int", "float", "float*", "float*", "float", "float*"};

      std::vector<OperatorArg> parsed_args;
      try {
        parsed_args = parseArguments(arguments, expected_types);
      } catch (const std::exception &e) {
        std::cerr << "Error parsing arguments: " << e.what() << std::endl;
        return false;
      }

      matmul_wrapper(parsed_args);

      updatePtrToMsgpack<float>(arguments[7], std::get<float *>(parsed_args[7]),
                                std::get<int>(parsed_args[0]) *
                                    std::get<int>(parsed_args[1]));

      std::cout << "Matrix multiplication completed by catzilla." << std::endl;
      return true;
    } else {
      return false;
    }
  }
  return true;
}

} // namespace quark

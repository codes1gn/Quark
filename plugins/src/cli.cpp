// #include "plugins.h"
// #include <iostream>
// #include <vector>
//
// int main(int argc, char *argv[]) {
//     if (argc < 4) {
//         std::cerr << "Usage: quark-plugins <executor> <opcode> [arguments...]" << std::endl;
//         return 1;
//     }
//
//     std::string executor = argv[1];
//     std::string opcode = argv[2];
//     std::vector<std::string> arguments;
//
//     for (int i = 3; i < argc; ++i) {
//         arguments.push_back(argv[i]);
//     }
//
//     std::string error_message;
//     bool success = quark::Plugins::execute(executor, opcode, arguments);
//
//     if (!success) {
//         std::cerr << "Error: " << error_message << std::endl;
//         return 1;
//     }
//
//     return 0;
// }
#include "options.h"
#include "plugins.h"
#include <iostream>

int main(int argc, char *argv[]) {
  Options options;

  // Add supported options
  options.addOption("e", "Executor name");
  options.addOption("w", "Operation workload");
  options.addOption("a", "Operation arguments");

  // Parse command line arguments
  if (!options.parse(argc, argv)) {
    options.printHelp();
    return 1;
  }

  // Get option values
  std::string executor = options.getOption("e");
  std::string opcode = options.getOption("w");
  std::vector<std::string> arguments = options.getArguments();

  // Check required options
  if (executor.empty() || opcode.empty()) {
    std::cerr << "Executor and opcode are required." << std::endl;
    options.printHelp();
    return 1;
  }

  // Call Plugins::execute
  std::string error_message;
  bool success = quark::Plugins::execute(executor, opcode, arguments);

  // Check execution result
  if (!success) {
    std::cerr << "Error: " << error_message << std::endl;
    return 1;
  }

  return 0;
}


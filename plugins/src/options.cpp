#include "options.h"
#include <iostream>

void Options::addOption(const std::string &name,
                        const std::string &description) {
  options[name] = {name, description};
}

bool Options::parse(int argc, char *argv[]) {
  for (int i = 1; i < argc; ++i) {
    std::string arg = argv[i];

    // Check if it's an option
    if (arg.size() > 1 && arg[0] == '-') {
      std::string name = arg.substr(1);

      // Check if the option exists
      if (options.find(name) == options.end()) {
        std::cerr << "Unknown option: " << arg << std::endl;
        return false;
      }

      // Get the value of the option
      if (name == "a") {
        arguments.push_back(argv[++i]);
      } else if (i + 1 < argc && argv[i + 1][0] != '-') {
        values[name] = argv[++i];
      } else {
        values[name] = "";
      }
    } else {
      // Save the argument
      arguments.push_back(arg);
    }
  }

  return true;
}

std::string Options::getOption(const std::string &name) const {
  auto it = values.find(name);
  return it != values.end() ? it->second : "";
}

const std::vector<std::string> &Options::getArguments() const {
  return arguments;
}

void Options::printHelp() const {
  std::cout << "Usage:" << std::endl;
  for (const auto &[name, option] : options) {
    std::cout << "  -" << name << " " << option.description << std::endl;
  }
}

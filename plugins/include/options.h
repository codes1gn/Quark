#ifndef QUARK_PLUGINS_OPTIONS_H_
#define QUARK_PLUGINS_OPTIONS_H_

#include <string>
#include <unordered_map>
#include <vector>

class Options {
public:
  // Add an option
  void addOption(const std::string &name, const std::string &description);

  // Parse command line arguments
  bool parse(int argc, char *argv[]);

  // Get the value of an option
  std::string getOption(const std::string &name) const;

  // Get all arguments
  const std::vector<std::string> &getArguments() const;

  // Print help information
  void printHelp() const;

private:
  struct Option {
    std::string name;
    std::string description;
  };

  std::unordered_map<std::string, Option> options;
  std::unordered_map<std::string, std::string> values;
  std::vector<std::string> arguments;
};

#endif // QUARK_PLUGINS_OPTIONS_H_

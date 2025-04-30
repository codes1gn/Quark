#include "arguments.h"
#include "serialisation.h"
#include <msgpack.hpp>

OperatorArg parseArgument(const std::string &arg,
                          const std::string &expected_type) {
  if (expected_type == "int") {
    return std::stoi(arg);
  } else if (expected_type == "float") {
    return std::stof(arg);
  } else if (expected_type == "double") {
    return std::stod(arg);
  } else if (expected_type == "float*") {
    return deserialisePtrFromMsgpack<float>(arg);
  } else if (expected_type == "double*") {
    return deserialisePtrFromMsgpack<double>(arg);
  } else {
    throw std::invalid_argument("Unknown expected type: " + expected_type);
  }
}

std::vector<OperatorArg>
parseArguments(const std::vector<std::string> &arguments,
               const std::vector<std::string> &expected_types) {
  if (arguments.size() != expected_types.size()) {
    throw std::invalid_argument(
        "Arguments size does not match expected types size");
  }

  std::vector<OperatorArg> parsed_args;
  for (size_t i = 0; i < arguments.size(); ++i) {
    parsed_args.push_back(parseArgument(arguments[i], expected_types[i]));
  }
  return parsed_args;
}

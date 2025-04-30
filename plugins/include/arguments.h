#ifndef QUARK_PLUGINS_ARGUMENTS_H_
#define QUARK_PLUGINS_ARGUMENTS_H_

#include <vector>
#include <string>
#include <variant>
#include <stdexcept>

using OperatorArg = std::variant<int, float, double, float*, double*>;

OperatorArg parseArgument(const std::string& arg, const std::string& expected_type);

std::vector<OperatorArg> parseArguments(const std::vector<std::string>& arguments, const std::vector<std::string>& expected_types);

#endif // QUARK_PLUGINS_ARGUMENTS_H_

// plugins/include/plugins.h
#ifndef QUARK_PLUGINS_H_
#define QUARK_PLUGINS_H_

#include <string>
#include <vector>

namespace quark {

class Plugins {
public:
  static void smoke_test();
  static bool execute(const std::string &executor, const std::string &opkind,
                      const std::vector<std::string> &arguments);
};

} // namespace quark

#endif // QUARK_PLUGINS_H_

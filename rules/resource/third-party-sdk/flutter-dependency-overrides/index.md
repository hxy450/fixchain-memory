# 根 pubspec.yaml 的 dependency_overrides

agent 会看到什么：读到插件解析记录（plugin-resolution.json）或各插件 solution 里列为未决、F3 的包；根 pubspec.yaml 的 dependency_overrides 给别的插件加了本地 path:，漏了某个未决包

## 规矩

- rule-29df1098cfd6｜写 dependency_overrides 时逐项对照未决插件，每个都要有本地 path 或可运行的失败实现｜读到：插件解析记录（`plugin-resolution.json`）或各插件 solution 里列为未决、F3 的包；写错：根 `pubspec.yaml` 的 `dependency_overrides` 给别的插件加了本地 `path:`，漏了某个未决包

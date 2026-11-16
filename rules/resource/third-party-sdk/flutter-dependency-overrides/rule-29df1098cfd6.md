# 写 dependency_overrides 时逐项对照未决插件，每个都要有本地 path 或可运行的失败实现

审的是：资源
触发（任一种）：
- 读到：插件解析记录（`plugin-resolution.json`）或各插件 solution 里列为未决、F3 的包；写错的样子：根 `pubspec.yaml` 的 `dependency_overrides` 给别的插件加了本地 `path:`，漏了某个未决包
适用范围：Flutter 复用路线下改根 pubspec.yaml 的 dependency_overrides 时
做法：
- 逐项对照未决插件清单，每个未决包在 dependency_overrides 下都有一项：本地兼容插件写 `<包名>:` 下 `path: ohos/flutter_plugins/<包名>`，或固定版本的 override
- 没有真实实现的包也要接上一个能运行、对每个方法显式回调失败的 OHOS 实现；只在文档里写「显式失败边界」不算
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 在根 pubspec.yaml 的 dependency_overrides 里给该插件加本地 path 后，链路在真机跑通：override 是 F3 插件真正接入的那一步（出处：卡里修好并验证过）
针对本应用要查的：
- 未决插件清单：插件适配阶段的插件解析记录和 solutions 目录下各包的 solution JSON，按 status、selected_layer 找；每个 F3 或未决的包都要在 dependency_overrides 里有同名的一项
来源：1 张卡，1 个应用
- case-075213be62b42126e39f（app-photo-shop-flutter）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4；取值 1 ← 诊断

# 源端容器色角色在目标 color 资源里缺失时，补齐或登记，不换成相邻的 surface

审的是：代码
触发（任一种）：
- 读到：源端用 `colorScheme.surfaceContainer`、`surfaceContainerLow` 等容器色角色（含 NavigationBar、ModalDrawerSheet 的默认容器色）；写错的样子：目标 color.json 里没有这个角色，代码换成相邻的 surface 色，注释写「spec 已登记差异降级」
适用范围：迁移 Material3 主题色到 ArkUI 资源，源端某个主题角色在目标 color 资源里还没有时
做法：
- 在 resources/base/element/color.json 和 resources/dark/element/color.json 补上这个角色，代码用 $r('app.color.<角色名>') 引用；补不了就登记资源缺口
- 规格里写的「差异降级」只用于它点名的对象（如窗口导航条染色），不扩大到组件容器色
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- $r('app.color.name')：引用本模块 color 资源的写法，name 是 color.json 里定义的资源名（出处：resource-categories-and-access.md，访问本模块资源或模块依赖的HAR资源）
- 限定词目录 dark：深色模式；light：浅色模式：深色下的角色色写在 dark 限定词目录的 color.json（出处：resource-categories-and-access.md，限定词目录）
- 底栏改为 surfaceContainer、抽屉面板改为 surfaceContainerLow：修复时按源端角色补齐后的取色（出处：卡里修好并验证过）
针对本应用要查的：
- 这个角色在亮、暗两套主题下的颜色：源工程 Compose 主题文件里的 lightColorScheme(...) / darkColorScheme(...)（或动态取色）里该角色的参数；没写的取该 material3 版本的默认色板；读出亮、暗两个颜色值，分别写进 base 和 dark 的 color.json
来源：1 张卡，1 个应用
- case-be2a579e8fcdcb8b0a16（jerboa）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2；取值 3 ← 诊断

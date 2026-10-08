# ui/theme/tokens

颜色与字体令牌的落地：按色值反查资源键、深色目录同步、深浅状态的可观察与系统栏图标、字族注册。

[上一级](../index.md)

## 本级经验

- [“零硬编码色值”只禁字面值，允许 $r 引用语义色](lesson-2e4279c4b82f06af64fd.lesson.md) · 阶段：spec/execute · 信号：$r('app.color, #RRGGBB, backgroundColor, fontColor
- [多字重字族逐文件 registerFont，入口只注册一次](lesson-046baeb5ffbb10a6abc5.lesson.md) · 阶段：execute · 信号：registerFont, familyName, familySrc, $rawfile
- [按源端实际色值与字号在资源中反查同值键，不按名选键](lesson-4e9507a2a793c5583aa8.lesson.md) · 阶段：execute · 信号：color.json, float.json, $r('app.color, $r('app.float
- [深浅主题状态放可观察对象，入口同步，组件渲染期读取](lesson-7b19b801e0f21481d1d6.lesson.md) · 阶段：execute · 信号：isSystemInDarkTheme, onConfigurationUpdate, colorMode, @ObservedV2
- [系统栏图标深浅按源端状态栏配置设置，不照搬模板](lesson-824031d5fddf81036b54.lesson.md) · 阶段：execute · 信号：setWindowSystemBarProperties, statusBarContentColor, navigationBarContentColor, ImmersionBar
- [追加主题色时同步写 dark 目录同名键，已有文件只追加](lesson-1e972af4bc7e27b23d9c.lesson.md) · 阶段：execute · 信号：color.json, resources/dark, resources/base, darkColors

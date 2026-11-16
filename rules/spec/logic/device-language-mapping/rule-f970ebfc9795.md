# 源端初始语言由未 await 的异步赋值和同步检测插件共同决定时，契约写 init 那刻实际生效的结果

审的是：规格
触发（任一种）：
- 读到：源端取设备语言的 `async` 函数没被 `await`，同时同步执行 `i18n.use(LanguageDetector).init({ lng: … })`，init 时 lng 还是空串；写错的样子：规格 AC 照异步分支的映射写（如裸 zh 强制映射为繁体），与 init 那刻由检测插件实际裁决的语言不同
适用范围：规格提取阶段，把源端初始语言检测逻辑翻成目标端系统语言解析契约时
做法：
- 按执行时序判断 init 那一刻 lng 实际取到的值：未 await 的异步赋值还没生效时，语言由 LanguageDetector 按 navigator.language 决定；把这个实际结果写进契约
- 有源端实机基线时用它核对契约，例如简体系统上基线显示简体
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- init 时 lng 为空，由 LanguageDetector 按 navigator.language 裁决，zh-CN 设备实际加载 zh-CN；异步分支的 zh→zh-TW 是竞态败者：源端实际生效的初始语言（出处：卡里修好并验证过）
针对本应用要查的：
- 源端 init 那刻语言变量的实际值：源工程的 i18n 初始化文件（.js/.ts），看取设备语言的函数是否被 await，以及 init 调用和它在模块里的执行先后；异步赋值在 init 之后才完成的，以检测插件的结果为准写契约
来源：1 张卡，1 个应用
- case-b3a0f2338f5f2dd14ef8（Countdate）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；取值 1 ← 诊断

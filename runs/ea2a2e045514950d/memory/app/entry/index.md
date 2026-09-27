# app/entry

入口 Ability（onCreate/onDestroy）：基础设施的显式初始化时机、需要补上的平台级守护，以及 module.json5 中入口 Ability 的 skills（深链）声明

[上一级](../index.md)

## 本级经验

- [入口 Ability 注册全局未捕获异常观察器，Android 源里没有对应代码也要补](lesson-c6132bf52c26ec226788.lesson.md)
  - 时机：入口装配阶段，改写 EntryAbility（或 AbilityStage）的 onCreate/onDestroy 并决定入口需要哪些平台级守护时
  - 情境：目标为 HarmonyOS Stage 模型应用，入口 UIAbility 由模板改写而来；Android 源没有可对照的全局异常处理，按源码迁移不会产生这段代码，而验收（如 ECAT crash_risk 规则）要求存在全局异常观察。
  - 例外：工程已在 AbilityStage 或其他入口注册了 errorManager 观察器或等效的崩溃监听
- [源端靠依赖注入或全局静态工具就绪的基础设施改成需显式 init 的封装后，在入口 onCreate 最早处调用，并确认启动期读写都晚于初始化](lesson-8a881c2e07f80f83447c.lesson.md)
  - 时机：网络、键值存储等基础设施实现与入口接线阶段：新建必须先 init 才能用的封装，或改写 EntryAbility.onCreate、宣告基础层完成时
  - 情境：源端网络 baseUrl 由 DI 模块在注入时带上、键值工具（SpUtils/MMKV 一类）全局静态可用，Application.onCreate 里看不到对应的初始化；目标端改为静态 HttpClient（baseUrl 默认空串）加 NetworkConfig.init()、偏好封装需先传入上下文；入口 Ability 由编排会话维护，Flutter 插件 onAttachedToEngine 等回调里也能拿到上下文。
- [迁移深链 intent-filter 时同时声明 module.json5 的 skills（actions、entities、uris），并用隐式 Want 验收](lesson-d77baa7494930d485425.lesson.md)
  - 时机：入口与导航接线阶段，把源端 Activity 的 VIEW/BROWSABLE intent-filter 迁成 UIAbility 的 Want 接收与路由解析时；以及规格提取阶段描述深链映射时
  - 情境：源 AndroidManifest 在启动 Activity 上声明 VIEW+BROWSABLE、http/https 与固定 host 的 intent-filter；目标 module.json5 的入口 Ability skills 仍是脚手架默认的 HOME 一项。

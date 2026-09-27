# app/entry

入口 Ability（onCreate/onDestroy）需要补上的平台级守护

[上一级](../index.md)

## 本级经验

- [入口 Ability 注册全局未捕获异常观察器，Android 源里没有对应代码也要补](lesson-c6132bf52c26ec226788.lesson.md)
  - 时机：入口装配阶段，改写 EntryAbility（或 AbilityStage）的 onCreate/onDestroy 并决定入口需要哪些平台级守护时
  - 情境：目标为 HarmonyOS Stage 模型应用，入口 UIAbility 由模板改写而来；Android 源没有可对照的全局异常处理，按源码迁移不会产生这段代码，而验收（如 ECAT crash_risk 规则）要求存在全局异常观察。
  - 例外：工程已在 AbilityStage 或其他入口注册了 errorManager 观察器或等效的崩溃监听

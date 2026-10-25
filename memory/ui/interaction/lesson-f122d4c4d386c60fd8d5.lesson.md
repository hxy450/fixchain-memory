# 行组件内挂了 onClick 时外层 ListItem 的 onClick 收不到点击：点击只设一个归属，动作经 @Event 传入或组件内不挂点击

ID：`lesson-f122d4c4d386c60fd8d5` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段，为可复用的列表行、设置行子组件定义点击接口，并在父页面为每行挂接动作时

## 适用情境

源端整行可点（PreferenceScreen 的 Preference/ListPreference 行、子屏入口等），目标把行抽成 @ComponentV2 子组件放进 ListItem 或容器；组件内部声明带空默认实现的 @Event（如 onTap: () => void = () => {}）并在内层 Row 挂 .onClick 调用它，调用点却不传该事件，而把真实动作挂在外层 ListItem().onClick 上。

## 例外与边界

- 父子确需响应同一次点击（如内层另有独立动作、外层仍要处理）时，按 ArkUI 手势规则给子元素改用 parallelGesture 等并行手势，不依赖冒泡

## 原因

ArkUI 的点击手势按子组件优先竞争：父子都命中时，子组件的 onClick 获胜，父容器的 onClick 不会触发，与 DOM 冒泡不同。内层 onClick 即使只调用空默认的 @Event，也会吞掉整行点击；编译与结构审计都能通过，只有实际点按才发现行无反应。

## 做法

1. 点击只给一个归属：行组件声明 @Event 并在内层 onClick 中调用时，每个调用点都传入本行动作，外层 ListItem 不再挂 onClick；动作由外层 ListItem 或容器处理时，行组件内部不挂 onClick、不声明对应 @Event。
2. 带空默认实现的 @Event 若被组件内 onClick 调用，逐个调用点核对是否传入；子组件内有 .onClick(() => this.onXxx()) 而调用处缺 onXxx、却在外层挂了 .onClick，即为被拦截的写法。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-f6ac0fc6805f2fc8ff14](../../../store/cases/case-f6ac0fc6805f2fc8ff14/690f0502298e3c25a20e6fc4b2f9eefbfbb15ea7c609091af99b0b66a33f684e.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`690f0502298e3c25a20e6fc4b2f9eefbfbb15ea7c609091af99b0b66a33f684e`

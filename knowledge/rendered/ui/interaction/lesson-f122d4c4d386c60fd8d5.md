# 行组件内挂了 onClick 时外层 ListItem 的 onClick 收不到点击：点击只设一个归属，动作经 @Event 传入或组件内不挂点击

## 何时使用

界面实现阶段，为可复用的列表行、设置行子组件定义点击接口，并在父页面为每行挂接动作时

## 适用情境

源端整行可点（PreferenceScreen 的 Preference/ListPreference 行、子屏入口等），目标把行抽成 @ComponentV2 子组件放进 ListItem 或容器；组件内部声明带空默认实现的 @Event（如 onTap: () => void = () => {}）并在内层 Row 挂 .onClick 调用它，调用点却不传该事件，而把真实动作挂在外层 ListItem().onClick 上。

## 例外与边界

- 父子确需响应同一次点击（如内层另有独立动作、外层仍要处理）时，按 ArkUI 手势规则在父容器（外层 ListItem 或行容器）上用 parallelGesture 绑定点击手势（mask 用默认的 GestureMask.Normal，不屏蔽子组件手势），子元素保留自己的 onClick，不依赖冒泡

## 原因

ArkUI 的点击手势按子组件优先竞争：父子都命中时，子组件的 onClick 获胜，父容器的 onClick 不会触发，与 DOM 冒泡不同。内层 onClick 即使只调用空默认的 @Event，也会吞掉整行点击；编译与结构审计都能通过，只有实际点按才发现行无反应。

## 做法

1. 点击只给一个归属：行组件声明 @Event 并在内层 onClick 中调用时，每个调用点都传入本行动作，外层 ListItem 不再挂 onClick；动作由外层 ListItem 或容器处理时，行组件内部不挂 onClick、不声明对应 @Event。
2. 带空默认实现的 @Event 若被组件内 onClick 调用，逐个调用点核对是否传入；子组件内有 .onClick(() => this.onXxx()) 而调用处缺 onXxx、却在外层挂了 .onClick，即为被拦截的写法。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因〕父子组件均绑定同一类手势时，子组件优先于父组件触发；父子都绑定点击时子组件的优先级高于父组件，父组件的点击不触发
- 〔原因〕除触摸事件 onTouch 外，所有手势与事件（含 onClick）都由基础手势或组合手势实现，按手势竞争决定谁响应，不是冒泡
- 〔原因 / 做法第 2 步〕@Event 没有被外部初始化时自动生成一个空函数作为默认回调；本地写了默认值时用本地默认函数，调用点不传时组件内调用它不报错也没有效果
- 〔例外与边界〕parallelGesture 绑定的是可与子组件手势同时触发的手势：父组件设置 parallelGesture 时父子相同的手势事件都可以触发；手势事件本身是非冒泡事件；mask 不传时默认 GestureMask.Normal（不屏蔽子组件手势）

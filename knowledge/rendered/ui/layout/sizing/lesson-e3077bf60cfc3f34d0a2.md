# layout_marginStart/End 写成 margin 的 start/end 时同一对象各边都用 LengthMetrics；不需要随语言方向翻转时改用 left/right 数值

## 何时使用

界面实现阶段，把 layout_marginStart/End、paddingStart/End 或 Compose padding(start/end) 一类方向相关边距写成 ArkUI margin/padding 时；维护映射参考的边距示例时

## 适用情境

源布局用 marginEnd/marginStart（常与 marginBottom 等写在同一控件上）；映射参考把它对到 .margin({ end }) 并给出纯数字示例。

## 原因

含 start/end 键的边距对象按 LocalizedMargin 解析，同一对象里的每一边（包括 top/bottom）都要求 LengthMetrics，写数字编译报 Type 'number' is not assignable to type 'LengthMetrics'。来源映射参考的示例直接写 margin({ end: 10 })，转换者照示例写出 { bottom: 16, end: 16 }，自检只核了 SDK 版本。

## 做法

1. 需要随布局方向翻转时写 .margin({ bottom: LengthMetrics.vp(16), end: LengthMetrics.vp(16) })，并从 @kit.ArkUI 导入 LengthMetrics；同一对象内不混用数字与 LengthMetrics。
2. 源应用未声明 supportsRtl（布局恒 LTR）或源端写的就是物理 left/right 时，统一写 left/right/top/bottom 数值（如 { bottom: 16, right: 16 }）；这只固定边距：ArkUI 组件 direction 不设时随系统语言方向，Row、Flex 等容器在从右向左的系统语言下仍会镜像，源端布局恒 LTR 时在这些容器上设 direction(Direction.Ltr)；源端 supportsRtl=true 且用 start/end 时按第 1 条保留逻辑方向，不就近改成 left/right。映射参考示例与 SDK 声明不一致时以声明为准，并修正参考。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36 的平台资源；android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1、2 步〕ArkUI 组件的镜像在 direction 为 Direction.Rtl，或 direction 为 Direction.Auto 且系统语言从右向左时生效；direction 不设时为 Direction.Auto（在 Column 上不生效）
- 〔做法第 1、2 步〕margin、padding 已适配镜像：要随镜像翻转须用 start/end 入参，left/right 是绝对方向，镜像时不翻转；Row、Column、Flex、List、Stack、Text 等组件默认适配镜像
- 〔做法第 2 步〕安卓 manifest 的 android:supportsRtl 不写时为 false；应用没有 RTL 支持时，View 的布局方向一律解析为 LTR，start/end 按左/右处理

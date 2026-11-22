# layout_marginStart/End 写成 margin 的 start/end 时同一对象各边都用 LengthMetrics；不需要随语言方向翻转时改用 left/right 数值

## 何时使用

界面实现阶段，把 layout_marginStart/End、paddingStart/End 或 Compose padding(start/end) 一类方向相关边距写成 ArkUI margin/padding 时；维护映射参考的边距示例时

## 适用情境

源布局用 marginEnd/marginStart（常与 marginBottom 等写在同一控件上）；映射参考把它对到 .margin({ end }) 并给出纯数字示例。

## 原因

含 start/end 键的边距对象按 LocalizedMargin 解析，同一对象里的每一边（包括 top/bottom）都要求 LengthMetrics，写数字编译报 Type 'number' is not assignable to type 'LengthMetrics'。来源映射参考的示例直接写 margin({ end: 10 })，转换者照示例写出 { bottom: 16, end: 16 }，自检只核了 SDK 版本。

## 做法

1. 需要随布局方向翻转时写 .margin({ bottom: LengthMetrics.vp(16), end: LengthMetrics.vp(16) })，并从 @kit.ArkUI 导入 LengthMetrics；同一对象内不混用数字与 LengthMetrics。
2. 源应用未声明 supportsRtl（布局恒 LTR）或源端写的就是物理 left/right 时，统一写 left/right/top/bottom 数值（如 { bottom: 16, right: 16 }）；源端 supportsRtl=true 且用 start/end 时按第 1 条保留逻辑方向，不就近改成 left/right。映射参考示例与 SDK 声明不一致时以声明为准，并修正参考。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 平台资源 android-37.0；源码 android-36.1；androidx.compose.ui:ui-android 1.10.3、1.12.0（字节码）。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕CommonMethod.margin(value: Margin | Length | LocalizedMargin): T、padding(value: Padding | Length | LocalizedPadding): T（Localized 两种入参 @since 12）；Margin = Padding = { top?, right?, bottom?, left?: Length }，各边可写数字（默认单位 vp）；默认值 0，参数为 Length 时四边同时生效
- 〔原因 / 做法第 1 步〕LocalizedPadding { top?: LengthMetrics; end?: LengthMetrics; bottom?: LengthMetrics; start?: LengthMetrics }（@since 12），LocalizedMargin = LocalizedPadding：对象里出现 start 或 end 时按这个类型检查，四边（包括 top、bottom）都只收 LengthMetrics；文档写 start 在从右至左显示语言下表示右边距、end 表示左边距
- 〔原因〕在 margin 的同一对象里给 bottom、end 写数字（如 { bottom: 16, end: 16 }）时编译报错，两处都是 Type 'number' is not assignable to type 'LengthMetrics'（HarmonyOS 6.1.1，API 24）
- 〔做法第 1 步〕LengthMetrics 的静态工厂（@since 12）：vp(value: number)、px(value: number)、fp(value: number)、percent(value: number)、lpx(value: number)、resource(value: Resource)，都返回 LengthMetrics；LengthMetrics 从 @kit.ArkUI 导入（import { LengthMetrics } from '@kit.ArkUI'）；文档示例写 .margin({ top: LengthMetrics.vp(40), bottom: LengthMetrics.vp(20), start: LengthMetrics.vp(30), end: LengthMetrics.vp(10) })
- 〔何时使用 / 做法第 1 步〕同族接口也接受 LocalizedPadding：CommonMethod.safeAreaPadding(paddingValue: Padding | LengthMetrics | LocalizedPadding): T（@since 14，默认 LengthMetrics.vp(0)）；BottomTabBarStyle.padding(value: Padding | Dimension | LocalizedPadding)；SubTabBarStyle 的 LocalizedPadding 是单独一个重载 padding(padding: LocalizedPadding)（@since 12）
- 〔做法第 1、2 步〕ArkUI 的镜像在组件 direction 为 Direction.Rtl，或 direction 为 Direction.Auto（默认值）且系统语言从右向左（如维吾尔语）时生效；padding、margin 等方向类通用属性要镜像须用 start/end 入参，left/right 是绝对方向、不镜像；Row、Column、List、Stack、Text 等组件已默认适配镜像，Canvas 只镜像文本绘制，XComponent 不支持镜像；direction 属性在 Column 上不生效
- 〔何时使用 / 适用情境〕安卓 paddingStart、paddingEnd、layout_marginStart、layout_marginEnd 的 format 都是 dimension；application 的 supportsRtl 声明应用能处理 RTL 布局，清单的 application 标签没写 supportsRtl 时默认 false
- 〔做法第 2 步〕安卓 View.resolveLayoutDirection 只在 ApplicationInfo.hasRtlSupport()（清单 supportsRtl=true）时才按父布局、layoutDirection 或 locale 解析出 RTL，否则解析结果恒为 LTR。从布局 XML 生成的 MarginLayoutParams 在没有 supportsRtl 时处于 RTL 兼容模式：只有 left/right 边距没定义时才把 start/end 当作 left/right 用，同时写了 left/right 的以 left/right 为准；有 supportsRtl 且写了 start 或 end 时，left、right 两侧都按 start/end 重算——LTR 下 left=start、right=end，RTL 下 left=end、right=start，没写的一侧为 0，同时写的 layout_marginLeft/Right 不再起作用（代码里 new MarginLayoutParams(w, h) 不进兼容模式）
- 〔何时使用 / 做法第 2 步〕Compose 的 LayoutDirection 取自宿主 View：AndroidComposeView 构造时先按 Configuration.getLayoutDirection()（随语言）取初值，View 解析 RTL 属性时 onRtlPropertiesChanged 把 View 解析出的布局方向设为 Compose 的 layoutDirection（ui-android 1.10.3、1.12.0 相同），所以清单没有 supportsRtl 时，挂到窗口完成解析后 Compose 的 padding(start/end) 也按 LTR 落到左/右

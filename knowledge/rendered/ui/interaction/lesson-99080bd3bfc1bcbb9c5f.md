# 源端禁用态只靠代码换背景、文字色固定时，不用 ArkUI .enabled(false)（会对整个组件降透明）：显式切换背景与投影，用 hitTestBehavior(HitTestMode.None) 或回调内判态拦截点击

## 何时使用

规格提取阶段为 setEnabled/android:enabled 切换的控件写转换决策时；界面实现阶段落实控件禁用态外观与点击拦截时

## 适用情境

源端在 setEnabled(false) 的同时 setBackgroundResource 换成没有 state_enabled 分支的灰色 drawable，textColor 是固定颜色而非 ColorStateList（AppCompat 按钮禁用时投影另归零）；映射参考把 setEnabled(false)/android:enabled 一律对到 .enabled(false)。

## 例外与边界

- 源端禁用外观本身来自 state_enabled 选择器或半透明（ColorStateList 的 disabled 项、Compose 组件默认禁用色）时，按源端色值显式写出；目标默认禁用透明度恰与源值一致时才直接用 .enabled()

## 原因

Android 的 setEnabled 只改状态，颜色由 drawable 与 textColor 选择器决定；ArkUI enabled(false) 会对整个组件（背景与文字）施加默认禁用透明度，源端“不透明灰底、纯白字”就变成发虚的浅灰。

## 做法

1. 先查源端禁用外观的来源：背景 drawable、textColor 有无 state_enabled 分支，按钮 stateListAnimator 在禁用时是否归零。只来自代码换背景时，规格写“禁用 = 换背景 + 不响应点击”，判据写禁用态取色等于源背景值、文字为源色。
2. 实现时不写 .enabled(false)：背景按启停态切换，禁用时投影置空，用 hitTestBehavior(HitTestMode.None) 拦截点击（或在回调内判态直接返回；None 只让本组件不参与触摸测试，不阻塞 Stack 里的下层兄弟和祖先，下层兄弟或祖先带点击处理、或设备接了键盘手柄时，用回调内判态）。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36 的平台资源和源码（android-37.0 平台资源同值）；androidx.appcompat:appcompat 1.1.0、1.8.0。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 2 步〕hitTestBehavior 不写时为 HitTestMode.Default：自身及子节点响应触摸测试，阻塞兄弟节点，不影响祖先节点；设为 HitTestMode.None 时组件自身不响应触摸测试，也不阻塞子节点、兄弟节点和祖先节点的触摸测试
- 〔原因〕CommonMethod.enabled 的声明注释只写了 false 时不响应点击操作，没有写外观变化；文档 enabled 示例里的禁用按钮另外显式写了 opacity(0.4)；文档说明禁用控制属性仅在按下时生效，交互过程中更改 enabled 无效
- 〔原因〕设备上组件设 enabled(false) 时，背景和文字被一起施加默认禁用透明度，不透明灰底、纯白字显示成发虚的浅灰
- 〔适用情境〕应用主题和控件没有另设按钮样式时，平台 Widget.Material.Button 提供 background=@drawable/btn_default_material、minHeight 48dip、minWidth 88dip、textAppearance=?attr/textAppearanceButton 和 stateListAnimator=@anim/button_state_list_anim_material
- 〔适用情境 / 做法第 1 步〕平台 button_state_list_anim_material：启用且按下时 elevation 2dp（button_elevation_material）、translationZ 4dp（button_pressed_z_material）；启用静止时 elevation 2dp、translationZ 0；未启用时 elevation 和 translationZ 都是 0，按钮禁用时投影消失
- 〔适用情境〕androidx.appcompat 1.1.0、1.8.0 中 Base.Widget.AppCompat.Button 在 API 21 起的 parent 是 android:Widget.Material.Button，自身不设 stateListAnimator，AppCompat 按钮在应用没有另设 stateListAnimator 时沿用平台的 button_state_list_anim_material（1.1.0 在 API 14–20 上 parent 是 android:Widget，没有这一动画）
- 〔适用情境〕安卓 View 换背景（setBackgroundDrawable / setBackgroundResource）时，只有新背景的 getPadding 返回 true 才用它的 padding 改写内边距；换成不带 padding 的 shape 背景时，原样式带来的内边距保留

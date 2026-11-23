# 源 manifest 未声明 android:supportsRtl 时布局方向恒为 LTR：有顺序或对齐语义的容器逐个显式 Direction.Ltr（Column 上不生效）

## 何时使用

规格提取与界面实现阶段，为带多语言资源的应用确定布局方向契约，新建按钮条、对话框面板等有顺序或起止对齐语义的容器时（含返修中用自绘面板替换系统弹窗）

## 适用情境

AndroidManifest 的 <application> 未声明 android:supportsRtl（安卓布局方向恒为 LTR）；应用含 fa 等 RTL 语言资源，或可能在 RTL 系统语言下运行；目标用 Row/Column 等容器实现按钮条、对话框或起始对齐的内容，未设 direction。

## 例外与边界

- 源端声明 android:supportsRtl="true"：按源布局的 start/end 语义让容器随语言方向翻转

## 原因

ArkUI 组件默认 Direction.Auto，跟随系统语言；来源实测子组件不继承父容器设置的方向，只给外层面板设 Ltr 时按钮条仍会镜像。未声明 supportsRtl 的源应用在 RTL 语言下保持 LTR，目标不显式固定，就会把负/正键顺序与起始对齐翻过来。

## 做法

1. 规格把“布局方向恒 LTR”写成目标契约；实现时在每个有顺序或对齐语义的容器（按钮条 Row 等 Row、Stack、Flex 容器）上显式 .direction(Direction.Ltr)，不只设在最外层；direction 在 Column 上不生效，对话框面板、alignItems(Start) 的内容区是 Column 时，给 Column 自己设 Ltr 没有效果，要给它里面有顺序或起止对齐语义的 Row、Stack 子容器逐个设 Ltr。

## 可选检查

- 在阿拉伯语等 RTL 系统语言下截图，确认按钮顺序与起始对齐和安卓一致。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36 的平台资源；android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔例外与边界 / 适用情境〕AndroidManifest 的 <application> 没写 android:supportsRtl 时取默认值 false，应用不声明支持 RTL 布局
- 〔适用情境〕应用没有声明 supportsRtl 时 View 处于 RTL 兼容模式（isRtlCompatibilityMode 返回 !hasRtlSupport()）：start/end 内边距按 left/right 解析，不看布局方向
- 〔原因〕组件没写 direction 时为 Direction.Auto；Auto 按照系统语言方向布局，不取父容器设置的方向；direction 取 undefined 或 null 时按默认值处理
- 〔做法第 1 步〕direction 属性在 Column 组件上不生效
- 〔原因〕设备上 RTL 系统语言下只给外层面板 Column 设 Direction.Ltr 时，其中的按钮条仍镜像；按钮条 Row 自己也设 Direction.Ltr 时按钮顺序保持 LTR

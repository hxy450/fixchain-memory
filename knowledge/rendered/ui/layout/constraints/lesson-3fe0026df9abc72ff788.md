# ConstraintLayout 改写成 Column 顺序流前先列出各子项锚点：锚父底、锚兄弟与双 0dp 比例子项都要保留语义

## 何时使用

界面实现阶段，把 ConstraintLayout 转成 Column/Row 顺序流或 Stack 层级，确定锚点边距与比例子项尺寸时

## 适用情境

源 ConstraintLayout 中有多个子项 constraintBottom_toBottomOf=parent（含 invisible 仍占位的行）、按钮上方的文字以 constraintBottom_toTopOf 锚在兄弟上、0dp×0dp 加 dimensionRatio 的子项夹在上下锚点之间；目标用 Column 顺序流、layoutWeight、Visibility.Hidden 或父 Stack 的 BottomStart。

## 例外与边界

- 第 2 步的常数底距只适用于兄弟行高度固定的情形；兄弟是 wrap_content、高度随文字、padding 或角标变化时，改用 RelativeContainer，以兄弟的 id 作锚（底边锚到兄弟顶边），margin 照源端写，不把当下量到的高度写成常数。

## 原因

顺序流里的 margin 相对前后兄弟，照抄锚父底的 margin 会叠在后续占位兄弟之上（偏高一个兄弟高度）；把锚兄弟简化成父容器底部对齐会压到兄弟上；双 0dp 比例子项的边长是 min(可用宽, 可用高)，只写 width('100%').aspectRatio(1) 在高度受限时会溢出。写者往往在思考中复述了这些约束，写码时仍按顺序堆叠。

## 做法

1. 转换前列出每个子项的锚点；多个子项锚父底时，用 Stack/RelativeContainer 按原 margin 贴底，或扣除后续流式兄弟的占位高度重算 margin。
2. 锚在兄弟上方的元素，底距 = 兄弟高度 + 其 padding + 自身 margin，不简化成父容器底部对齐。
3. 双 0dp 加 dimensionRatio 的子项按 min(可用宽, 可用高) 定边长：高度受限时写 height('100%').aspectRatio(r) 并限制宽度，源里的上下 margin 放到承担 layoutWeight 的容器上。
4. 注释里列出的尺寸与边距逐项对照实际修饰链，注释有而代码没有的按缺失处理。

## 可选检查

- dumpLayout 核对比例子项不超出其容器、锚底子项到内容层底的距离等于源 margin。

来源支持：2 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码；androidx.constraintlayout:constraintlayout 2.2.2。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕Visibility.Hidden 隐藏但参与布局占位，Visibility.None 隐藏且不占位
- 〔适用情境〕安卓 View.INVISIBLE 不可见，但仍为布局占位
- 〔做法第 1 步〕alignRules 只在父容器是 RelativeContainer 时生效
- 〔做法第 1 步〕RelativeContainer 中子组件的 margin 表示到该方向锚点的距离，没有设置某个方向锚点时该方向的 margin 不生效；父容器作锚点时标识为 __container__
- 〔做法第 3 步〕aspectRatio = width / height：只设 width 时 height = width / aspectRatio；只设 height 时 width = height × aspectRatio；width、height 都设时 height 按 width / aspectRatio 重算，显式写的 height 不生效
- 〔做法第 3 步〕设了 aspectRatio 后组件宽高受父组件内容区大小限制；constraintSize 的 maxWidth、maxHeight 优先级高于 aspectRatio，冲突时按 constraintSize
- 〔做法第 3 步〕纵向空间受限的 layoutWeight 容器里，Image 写 width('100%').aspectRatio(1) 时按宽度算出高度，测得的高度超出容器
- 〔适用情境 / 做法第 3 步〕ConstraintLayout 的 layout_constraintDimensionRatio 属性格式是 string（如 "1:1"），目标 aspectRatio 接收的是宽除以高的数值
- 〔做法第 2 步〕Stack 的 alignContent 是所有子组件在容器内的统一对齐方式（默认 Alignment.Center，非法值按默认处理），不让某个子组件参照兄弟定位

# 单视图对父容器居中、兄弟单向悬挂时（ConstraintLayout 单向约束、RelativeLayout layout_below），用 RelativeContainer 或不占行高的下挂层复刻，不用 Column 整组居中

## 何时使用

规格提取阶段把 ConstraintLayout 约束翻译成容器与定位决策，或页面实现阶段落定容器时；转换 RelativeLayout 控件排（按钮 layout_centerVertical、标签 layout_below）时

## 适用情境

源 ConstraintLayout 中一个子视图以 start/end/top/bottom 四向锚定 parent 自身居中，另一个兄弟只以 constraintTop_toBottomOf 等单向约束挂在它下方，兄弟之间没有双向约束。也包括 RelativeLayout 控件排：按钮 layout_centerVertical，标签以 layout_below 挂在各自按钮下方，兄弟之间有固定 margin。

## 例外与边界

- 兄弟之间有双向约束构成 chain 时，按 chain 语义（chainStyle）另行转换，不适用本条

## 原因

只有相邻视图互相双向约束才构成 chain；单向悬挂的兄弟不参与居中，被居中的只有锚定 parent 的那个视图。改成 Column 整组居中后，该视图中心会上移 (间距 + 兄弟高度) / 2。来源中规格把这种布局概括成“垂直居中链”：结构段写对了锚点，决策表却选了 Column 居中，项目级映射基线也写成“居中约束链 → Column 居中”，实现照做。另一应用中，城市卡的天气图标与描述块同时约束到 parent 的 start 与 end、在整卡中居中，转换者却把它放进 Row 里 Blank() 之后，天气信息被推到右侧、挨着温度。

## 做法

1. 规格提取时逐个子视图记下纵向锚点指向 parent 还是兄弟，再判断是否构成 chain；把决策写成“A 在容器内自身居中，B 以 top 锚 A 底部加间距”，写完与同文件的页面结构段对账；项目级映射基线里的笼统映射按同一规则改成按约束区分。
2. ArkUI 用 RelativeContainer：A 设 .alignRules({ middle: { anchor: '__container__', align: HorizontalAlign.Center }, center: { anchor: '__container__', align: VerticalAlign.Center } })；B 设 .alignRules({ middle: { anchor: '__container__', align: HorizontalAlign.Center }, top: { anchor: '<A 的 id>', align: VerticalAlign.Bottom } }).margin({ top: <源间距> })；被锚定的子组件要设 id。
3. 实现阶段若规格给的是 Column 整组居中，先用源 XML 的 constraint 属性核对；与源约束冲突时按源约束实现，并在转换报告标出。
4. 列表项中同时约束到 parent 首尾的信息块在整卡居中：用 Stack 居中叠放或 RelativeContainer 居中对齐，不放进用 Blank() 分隔的横向 Row；贴 parent 末端的兄弟单独按末端锚定。
5. RelativeLayout 控件排中按钮保持源尺寸，由 Row alignItems(VerticalAlign.Center) 对齐；layout_below 的标签做成不占行高的下挂层（Stack 加 position，或 RelativeContainer alignRules），逐个兄弟补齐源 margin，不用统一的大槽位把图标和标签一起居中。

## 可选检查

- 对居中结果有疑问时，用布局 dump 比较被居中视图的中心与容器内容区中心，单视图居中时两者应重合；无需另起截图任务。

来源支持：3 张卡 · 3 次迁移 · 3 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 androidx.constraintlayout:constraintlayout 2.2.2。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕ConstraintLayout 的 layout_constraintTop_toBottomOf 属性格式是 reference|enum：取兄弟视图 id 时锚兄弟，取 parent 时锚父容器
- 〔做法第 2 步〕RelativeContainer 的子组件要有唯一的组件标识（id）才能被指定为锚点；父容器 RelativeContainer 的标识默认为 __container__
- 〔做法第 4 步〕Stack 不写 alignContent 时子组件按 Alignment.Center 居中叠放
- 〔做法第 5 步〕Row 的 alignItems 不设时为 VerticalAlign.Center
- 〔做法第 5 步〕position 是相对父组件内容区的绝对定位；父组件为 Row、Column 或 Flex 时，设了 position 的子组件不占位
- 〔做法第 5 步〕offset 相对组件原位置偏移，只在绘制时调整位置，布局仍按原位置占位

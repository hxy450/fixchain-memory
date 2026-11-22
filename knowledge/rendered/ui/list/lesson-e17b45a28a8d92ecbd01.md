# 多类型 Adapter 承载的页面按全部 item 布局和 handleXxx 分支建区块：默认态、文案模板与附属子卡都来自绑定代码

## 何时使用

界面实现与返修重建阶段，把主体内容由 RecyclerView 多类型 Adapter 承载的 Android 页面转成 ArkUI 页面、确定各区块结构与背景层级时

## 适用情境

源页面布局只有头图与 SwipeRefreshLayout/RecyclerView 外壳，首屏卡片、趋势图、网格等区块分散在 addItemType 登记的 item 布局与 handleXxx/convert 绑定里：默认选中态、setText 拼接的文案模板（如“平均温度X”“N天降温/M天升温”）、按条件 visibility 显示的附属子卡；UI 快照可能是合成的，item 布局清单可能为空。

## 原因

只凭区块标题或绑定代码片段推断卡片，会写出固定高度的占位列表、只有标题的卡片，把原始数值 toString 输出，还会删掉附属子卡；RecyclerView 本身无背景、叠在头图之上的层级也容易被一个不透明列表背景盖住。来源为同一应用的两次写入：生成期转换者读到 Adapter 有七类区块，却没打开任何 item 布局就写盘，内容列表背景遮住头图、15日区只有文字列表、40日区只有标题；返修重建者读到 handleForty/handleLife 后，仍把 40 日文案写成原始数值、删掉旧入口却没建黄历宜忌子卡。

## 做法

1. 从 addItemType/onCreateViewHolder 列出全部 item 布局并逐个读取，按 item 布局实现区块；规格提取时把这些 item 布局登记进页面规格的布局清单。
2. 逐个 handleXxx 抄录 setText 的文案模板和全部分支、visibility 控制的子卡、默认选中态；默认分支就是首屏形态，切换控件要真正切换渲染内容。删除旧骨架入口前，先找到它在源端对应的完整区块并用等价组件替换。
3. 源 RecyclerView 与根容器没有背景、头图在下层时，目标滚动内容层保持透明，只给各卡片设置自身背景。

来源支持：2 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 3 步〕Stack 的子组件按声明顺序依次入栈，后声明的子组件渲染层级更高、覆盖前面的子组件；写在头图之后的内容层设了不透明背景就会盖住头图
- 〔做法第 2 步〕安卓 View.INVISIBLE 不可见但仍占布局空间，View.GONE 不可见且不占布局空间；ArkUI Visibility.Hidden 隐藏但参与布局占位，Visibility.None 隐藏且不占位

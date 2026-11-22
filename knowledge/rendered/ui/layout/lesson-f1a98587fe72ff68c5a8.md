# 页面转换逐项落实源 XML 的 gone 节点（代码只绑点击、没有设为可见的入口也不渲染）、固定尺寸点击容器与 tools:listitem 行布局

## 何时使用

页面转换阶段，把 Android 页面 XML 翻译为 ArkUI 结构与几何时；迁移标题栏或工具栏图标按钮并决定是否显示时

## 适用情境

源布局含 visibility=gone 的标题等节点、固定尺寸的点击容器（如 40×48dp 的返回 ImageView），列表 RecyclerView 用 tools:listitem 引用独立的 item 布局；迁移用的页面快照是合成的，可能把 gone 节点列为可见文本。 也包括 Activity 对 visibility=gone 的标题栏图标 findViewById 并绑定跳转（如打开搜索页），全文没有 setVisibility(VISIBLE)；目标工程其他页面已有同类入口的现成写法。也包括页面声明并在更新函数中维护某个展示状态（如倍速文本），build 中却没有消费它的组件。也包括 gone 的结果标题行容器：Activity 只改它子控件的文案或可见性，从不让容器本身可见；合成 view.xml 列出了该节点却没有 visibility 属性。

## 例外与边界

- 判定「从不设为可见」时，Kotlin 源码里的写法要一并算上：属性赋值 xxx.visibility = View.VISIBLE，以及 androidx core-ktx 的 isVisible = true、isGone = false、isInvisible = false；只搜 setVisibility( 会漏掉这些，把运行时会显示的节点当成常驻 gone 删掉。

## 原因

只按快照或主布局写，会渲染源端隐藏的节点、把点击区缩成图标大小，列表行也缺少 item 布局里的图标与右侧信息列。来源中转换者读到了 40×48dp 返回区、visibility=gone 的“搜索结果”标题和 tools:listitem 引用，写出的返回图只有 16×16，标题无条件显示，也没有打开 item 布局，结果行缺地址图标和距离列。 点击监听只说明代码可达，不说明控件可见；照搬目标工程其他页面的入口惯例，会把源端隐藏的入口生成为可见按钮。另一应用的分类页标题栏即如此：写者首稿按源布局留了空占位，后来改成照其他页面加了搜索入口。

## 做法

1. visibility=gone 的节点不渲染（或按源端条件显示）；快照可见文本与源 XML 可见性冲突时以源 XML 为准。
2. 固定尺寸的点击容器按其宽高作为热区，图标尺寸另按 src 与 scaleType 取。
3. 列表行结构打开 tools:listitem（或适配器 inflate 的）item 布局，取图标、文字层级与右侧列。
4. 判定图标按钮是否显示时，先看 XML 初始 visibility，再查代码中对该 View 的全部 setVisibility；只有 findViewById 与点击监听、没有 VISIBLE 分支的 gone 入口不生成。目标工程其他页面的写法只决定怎样实现，不决定源页是否有该入口；有截图时新增可见元素前先用截图核对，协调者追加的入口要求与源布局或截图冲突时先回报冲突。
5. 源端靠左右对称让中间控件居中时，隐藏一侧用同尺寸空占位（如返回键对侧的 44×44 空 Row）保持居中，不放可点击图标。
6. 以源布局 View id 为清单逐个生成渲染节点；每个声明并赋值的展示状态，在 build 中都要有消费它的组件。
7. 子控件的 setText、setVisibility 不代表父容器会显示：对 gone/invisible 的容器检索它自身 id 是否被设为可见，没有就不渲染或写 Visibility.None；转换前按页面状态（有数据、为空、结果、无结果）列出各自可见的标题与删除入口，确认同一语义只出现一次。

来源支持：4 张卡 · 4 次迁移 · 4 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-37.0 的平台资源。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1、4、7 步〕安卓 android:visibility 不写时为 visible（0）；invisible（1）不显示但布局时留出空间；gone（2）完全隐藏，如同没有加进布局
- 〔做法第 1、7 步〕ArkUI Visibility.Hidden 隐藏但参与布局占位；Visibility.None 隐藏且不参与布局、不占位

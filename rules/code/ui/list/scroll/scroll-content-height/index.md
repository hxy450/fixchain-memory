# Scroll 内容区的高度和纵向位置

agent 会看到什么：读到 ScrollView / NestedScrollView 或权重剩余区里的内容、空态和等高列；产物里 Scroll 内容 Column 上的 .height('100%')、.layoutWeight、constraintSize({ minHeight })、justifyContent

## 规矩

- rule-c86586ba819e｜ScrollView 转 Scroll 时，内容 Column 写 minHeight 100% 并顶对齐｜读到：ScrollView 或 NestedScrollView 包纵向 LinearLayout，LinearLayout 没写 android:gravity，子项自上而下，内容可能不足一屏；写错：目标 Scroll() { Column() { … } } 的 Column 没写 constraintSize({ minHeight: '100%' }) 和 justifyContent(FlexAlign.Start)，短内容整体纵向居中、首块离开顶部
- rule-6bbf54ad187b｜源空态是 wrap_content 且未在父布局居中的滚动容器时，目标靠上放，不写全高居中｜读到：空态容器是 NestedScrollView / ScrollView，android:layout_height="wrap_content"，在 RelativeLayout 里没声明居中；内层 LinearLayout 写 android:gravity="center"；写错：目标空态外层 Column 写 .height('100%') 加 .justifyContent(FlexAlign.Center)，内容在整个内容区垂直居中
- rule-51b3a6325da3｜权重剩余区里居中的空态放进 layoutWeight(1) 区居中，不靠 Scroll 内的 100% 高｜读到：android:layout_height="0dp" + android:layout_weight="1" 的容器里，RecyclerView 与 match_parent、android:gravity="center" 的空态 TextView 叠放，空态按数据显隐；写错：空态 Text 写在 Scroll 的内容 Column 里并设 .height('100%')，空态贴顶不居中；weight=1 的剩余区没有对应的 layoutWeight(1)
- rule-0f8130c15a06｜右列 match_parent 随左卡等高时，用左卡 onSizeChange 的实测高绑右卡 height｜读到：水平 LinearLayout 里右列 android:layout_height="match_parent"，随左侧 wrap_content 的卡片等高；右列内子卡 wrap_content + layout_weight，兄弟容器 android:visibility="gone"；整行在 NestedScrollView 里；写错：右卡在 Scroll 内写纵向 .layoutWeight(1) 或 .height('100%')（被撑到整屏），或者改成按字号行高估算的常量 .height(<常量>)
- rule-57dbfdbf312a｜用 Scroll 承接 NestedScrollView 时显式写 .align(Alignment.Top)｜读到：源布局用 NestedScrollView（或 ScrollView）承接页面内容，内容从顶部排起；写错：目标 Scroll 没写 .align(Alignment.Top)；内容短于视口时整列下沉，头部脱离工具栏
- rule-1f32ddd32757｜滚动页转 Scroll 且源内容贴顶时，子容器写 constraintSize({minHeight:'100%'})｜读到：match_parent 的 NestedScrollView/ScrollView 里放 wrap_content 内容，首块用 app:layout_constraintTop_toTopOf="parent" 贴顶，内容常不满一屏；写错：Scroll 的子 Column 只写 .width('100%')，没有 .constraintSize({ minHeight: '100%' }) 这类约束，内容不满一屏时整块垂直居中
- rule-d4f535bc0fea｜固定高度键盘配 layoutWeight 中间区时，加条件行前确认有空间，否则改滚动或固定位置｜写错：固定高度的键盘和 `layoutWeight(1)` 的中间区放在同一个 `Column` 里，中间区末尾追加条件行（`if (...) { Text(...) }`），中间区没有 `Scroll`
- rule-e860e3915764｜源内容区顶部流式、目标是 Scroll 包 Column 时，子 Column 加 minHeight 和顶部对齐｜读到：源端内容区是 IonContent（ion-content），内容从顶部往下流式排布；写错：目标 Scroll() { Column() { … } } 的子 Column 只有 width、padding、alignItems(HorizontalAlign.Center)，没有 constraintSize({ minHeight: '100%' }) 和 justifyContent(FlexAlign.Start)，内容短于一屏时整体被垂直居中

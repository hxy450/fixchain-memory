# 随内容高的父容器里的 height('100%')

agent 会看到什么：读到 NestedScrollView、wrap_content 的槽位或弹层根、被嵌入的 Fragment 布局根里按内容取高的子树；产物里 Scroll、bindSheet 内容或子组件 build() 根和各状态分支上的 .height('100%')、依赖父高的 .layoutWeight

## 规矩

- rule-060c9f538228｜Scroll 或无高度 Column 里的子树不写 height('100%') 和 layoutWeight｜读到：源端 NestedScrollView 里，或 android:layout_height="wrap_content" 的 FrameLayout 槽位里，子 View 写 match_parent（实际按内容取高）；写错：目标 Scroll() { Column() {...} } 或未设 height 的 Column 里，子树（含嵌进去的子组件 build() 根节点和各状态分支）写 .height('100%') 或依赖父高的 .layoutWeight(1)
- rule-8b3aac8a28d6｜被嵌入子组件的源布局根和状态容器是 wrap_content 时，根和各状态视图不写 height('100%')｜读到：将被宿主嵌入的子组件（规格写 `page_type=sub_component`，源端是 Fragment 布局）：根节点、内层容器和空态容器都是 android:layout_height="wrap_content"；写错：@ComponentV2 / @Component 的 build() 根 Column，以及 loading / empty / error / 列表态的外层写了 .height('100%')
- rule-37df5087d927｜bindSheet 内容组件的根 Scroll / Column 不写 height('100%')，随内容高度｜读到：源弹层根布局 android:layout_height="wrap_content"，或是 match_parent 但位于 BottomSheet 的 wrap_content 容器里；写错：bindSheet 内容组件的根 Scroll 或 Column 写了 .height('100%')

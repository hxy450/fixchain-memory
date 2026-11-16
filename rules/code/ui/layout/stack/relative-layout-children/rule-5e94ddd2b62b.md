# 源控件排里每个 ImageButton / TextView 都要有渲染节点，赋值的展示状态要在 build 里被读

审的是：代码
触发（任一种）：
- 读到：源布局 RelativeLayout 控件排里 ImageButton 旁有 TextView 标签（android:layout_below 挂在按钮下方的速度、秒数等文字）；写错的样子：目标声明了 @Local / @State 展示状态并在更新函数里给它赋值，build() 里却没有读它的 Text(...)；或注释写着「按钮 + 标签」，对应的 Column 里只有 Image
适用范围：把安卓 RelativeLayout 控件排（按钮带文字标签）转写成 ArkUI 组件时
做法：
- 逐个对照源布局里的 View id，确认每个 ImageButton / TextView 在 build() 里都有对应的组件
- 凡是声明并在更新函数里赋值的展示状态，在 build() 里找到消费它的组件，如 Text(this.<状态名>)；找不到就补上对应的 Text
来源：1 张卡，1 个应用
- case-5b7b00a1deb25ed0b8d3（AntennaPod）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断

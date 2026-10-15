# arkts/ui-syntax

声明式 UI 语法：build() 与 @Builder 中可写的组件、条件与循环渲染形式（多行、花括号、不加分号），stateStyles 状态值的合法写法，以及 justifyContent 等容器专属属性的适用范围

[上一级](../index.md)

## 本级经验

- [build() 与 @Builder 里每个组件、条件与循环渲染各占独立行：if/else 带花括号、块后不加分号，含组件语法的方法声明为 @Builder](lesson-08e71bb72d05b1d79d28.lesson.md)
  - 时机：界面实现阶段，整页编写或重写 ArkTS 页面的 build() 与可复用组件片段，并在交付前自检语法时
  - 情境：页面含卡片片段、加载/空/错误或有图/无图等条件渲染与 ForEach/Repeat 列表；写者倾向把组件树压成一个方法一行、用分号拼接，或把卡片写成普通 private 方法；生成期常不编译。
- [justifyContent/alignItems 只属于 Column/Row/Flex：替换容器头时连同尾部修饰链核对，Stack 的内容对齐用 alignContent](lesson-18d9c9a34c1952f43f53.lesson.md)
  - 时机：界面实现阶段，替换容器类型（如把 Column 改成 Scroll 包裹内容）或为 Scroll、Stack 等容器设置内容对齐时
  - 情境：页面把占位 Column 改成 Scroll 包裹内容而补丁只替换了容器头，或把 Compose Box(contentAlignment)、FrameLayout 居中布局迁成 Stack，并在容器修饰链上写 justifyContent、alignItems。
- [stateStyles 各状态只写 @Styles 方法引用、全局 @Styles 函数名或以点号开头的内联样式块，不写 { 属性名: 值 } 对象：后者编译放行、页面渲染即崩](lesson-39d1dee415d4a252fc5c.lesson.md)
  - 时机：界面实现阶段为容器写按压等状态样式时；编译修复阶段处理 .stateStyles 报 10905203（'.stateStyles' doesn't conform standard）并选择替代写法时
  - 情境：ArkUI 容器用 .stateStyles({ pressed: … }) 复刻源端列表选择器等按压反馈；d.ts 中 StateStyles 各字段类型为 any，ets-loader 只检查单属性对象字面量的形状，并把该属性的值当作属性调用来绑定；同一 .ets 文件里可能还有其他 struct（如页内弹窗组件）。

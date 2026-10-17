# ui/libraries

由三方 UI 库（Gradle AAR 依赖）渲染或承载的页面、控件与提示：取库工件核对几何与行为，再决定复刻或登记差异

[上一级](../index.md)

## 本级经验

- [UI 由三方库渲染、仓库只有调用面时，先取库工件（AAR 或版本 tag 源码）核对几何与行为再定映射；取不到登记阻塞，不按库名自研近似](lesson-f79082832a2fb18c8754.lesson.md)
  - 时机：规格提取阶段，为 build.gradle 依赖的三方 UI 库（引导页、日期/时间选择器、取色器、图片查看器、提示条、FAB 菜单、清单编辑器、自定义 TextView 子类、对话框库）写转换决策与跨栈映射行时；实现阶段按“自研 / 原生组件替代 / Toast”一类映射行实现该库承载的组件，或准备以“库源不可见”登记占位时
  - 情境：Activity 继承库基类（如 extends AppIntro2），布局或 UI 快照只剩库的自定义 View 类名（SublimePicker、holocolorpicker.ColorPicker、GalleryViewPager、FloatingActionsMenu、库 TextView 子类），或应用侧只保留库的 Style/Configuration 常量与配置调用（showCheckMarks、gatherLinksForText、Lib.makeText(...).show()）；几何、动画、手势、队列、截断与序列化算法都在库内，目标端没有同名库，规格准备写“自研 / 原生组件替代 / 默认样式即可对齐”并标 Auto 或 HARD；本机 Gradle 缓存可能尚无该 AAR。
  - 例外：当前任务或已批准决策明确只要求功能等价、接受与库行为不同：仍把与库行为的差异逐项写进决策，不标等价

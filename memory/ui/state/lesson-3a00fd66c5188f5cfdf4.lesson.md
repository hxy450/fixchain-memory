# 负责上抛自身可见性的组件必须常建：不用 if 包住它，隐藏态用零高加 clip 或 opacity，不依赖 Visibility.None 保证创建

ID：`lesson-3a00fd66c5188f5cfdf4` · 版本：2

[本主题](index.md)

## 何时使用

界面实现阶段，翻译“容器初始隐藏、内部组件常驻并自行通知宿主显示”的结构，或向他人预留的条件槽位嵌入组件时

## 适用情境

源容器 visibility=gone，但内部 Fragment 在 onCreate 即挂载，并由它调用宿主的可见性方法；目标用 if 或 Visibility 控制容器，或把该组件填进由宿主条件包住的槽位。

## 例外与边界

- 该组件不负责上抛可见性，由宿主或其他常建组件决定显隐：按宿主状态用 if 条件构建即可

## 原因

ArkUI 中 if 条件为假时其中的组件不实例化，aboutToAppear 不执行；唯一能把可见性置真的组件被挡住时就不存在，形成死锁。Visibility.None 是否阻止实例化有两份相反依据：SDK 的 ets-loader 编译产物把 visibility 绑在包装节点上并照常创建实例（common.d.ts：aboutToAppear 在实例创建后、build 前调用）；真机实测却观察到 Visibility.None 下自定义组件未执行 aboutToAppear，强制 Visible 后才执行。带自定义布局（onMeasureSize/onPlaceChildren）的组件 aboutToAppear 在布局过程中才调用，不占位时也不能假定已执行。

## 做法

1. 不用 if 包住该组件；隐藏态优先用高度 0 加 clip，或 opacity 配合 hitTestBehavior 控制显示与命中，让组件始终参与构建与布局。
2. 确需用 Visibility.None/Hidden 表达隐藏时，先在当前工具链上以隐藏态启动，在该组件 aboutToAppear 打日志确认已执行；未执行就改用上一步写法。
3. 向宿主槽位嵌入组件前读取包住槽位的构建条件；若条件依赖本组件上抛的状态，先改宿主为常建或登记接线问题。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-590e7a719e7ced6a558d](../../../store/cases/case-590e7a719e7ced6a558d/a06d50e4608fc813ee38b5709db5b02832a251760aec789ba9ab960201db143a.json) · 结论：diagnosis, recommendation:1, recommendation:4
  卡片版本：`a06d50e4608fc813ee38b5709db5b02832a251760aec789ba9ab960201db143a`

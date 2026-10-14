# ui/containers

抽屉与对话框等容器：默认遮罩、几何与挂载层级

[上一级](../index.md)

## 本级经验

- [AlertDialog类自定义弹窗做成页面根的整窗层，按框架规则定宽](lesson-2550fef591d2f4a127c2.lesson.md)
  - 时机：规格提取、执行派工与界面实现阶段，为AlertDialog/DialogFragment自定义布局弹窗决定ArkUI挂载层级、遮罩范围与面板宽度时
  - 情境：源以AlertDialog.Builder.setView承载自定义布局（独立窗口）；目标改为组件树中条件渲染的自定义弹层，而触发方与回调消费方是嵌在页面里的子组件。
  - 例外：改用CustomDialogController等本身即窗口级的弹窗能力时，挂载层级由框架负责，只需按框架规则核对宽度与遮罩
- [DrawerLayout换成SideBarContainer时补齐源容器的默认行为](lesson-b7a4c0ab34ad22b11856.lesson.md)
  - 时机：界面实现阶段，把DrawerLayout抽屉页转成ArkUI SideBarContainer并设置侧栏宽度、分隔线、内容对齐与遮罩时；规格阶段声称两者语义对齐时同样适用
  - 情境：源根布局为DrawerLayout，抽屉是wrap_content宽的ScrollView；目标用SideBarContainer(Overlay)加Scroll。

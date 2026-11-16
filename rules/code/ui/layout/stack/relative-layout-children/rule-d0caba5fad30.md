# 源端空态挂到根 RelativeLayout 并 CENTER_IN_PARENT 时，目标空态放根 Stack 居中

审的是：代码
触发（任一种）：
- 读到：空态视图由辅助类 addView 到页面根 RelativeLayout，LayoutParams 上 addRule(RelativeLayout.CENTER_IN_PARENT)；规格 anchors 里列了这个辅助类；写错的样子：空态写在列表所在的子 Stack 或 List 容器里，没有放在页面根 Stack 里居中
适用范围：安卓页面用辅助类把空态挂到根布局并居中、迁成 ArkUI 页面时
做法：
- 按源端辅助类的挂载规则（addView 到哪个父布局、加了哪条 addRule）决定容器：CENTER_IN_PARENT 对应放进页面根 Stack 的直接子组件，靠 Stack 默认居中或写 .alignContent(Alignment.Center)
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- RelativeLayout.CENTER_IN_PARENT = 13：子视图相对父 RelativeLayout 的边界居中（出处：android.widget.RelativeLayout#CENTER_IN_PARENT）
- StackOptions.alignContent?: Alignment，@default Alignment.Center：Stack 不写对齐时子组件居中（出处：鸿蒙 SDK 的 ets/component/stack.d.ts，StackOptions.alignContent）
- alignContent(value: Alignment): StackAttribute：Stack 上显式写对齐的属性方法（出处：鸿蒙 SDK 的 ets/component/stack.d.ts，StackAttribute.alignContent）
- alignContent(value: Alignment): FolderStackAttribute：同族接口：FolderStack 的对齐（出处：鸿蒙 SDK 的 ets/component/folder_stack.d.ts，FolderStackAttribute.alignContent）
针对本应用要查的：
- 空态挂到哪个父布局、怎么定位：源工程里规格 anchors 列出的空态辅助类（Java/Kotlin），找 addView 和 LayoutParams.addRule 那段；读出父布局是哪一层、规则是 CENTER_IN_PARENT 还是别的，按它选目标容器和对齐
来源：1 张卡，1 个应用
- case-f226842558d82e3f3ad9（AntennaPod）：做法第 1 步 ← 建议 5、诊断

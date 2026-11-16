# 源控件没写背景或写 @null 时，顺父容器和主题查出透出的底色，目标这一层不垫色

审的是：代码
触发（任一种）：
- 读到：源控件和它的父容器没写 android:background，或写了 android:background="@null"（RecyclerView、FrameLayout、EditText、SurfaceView 等）；写错的样子：目标对应组件上多了源端没有的 .backgroundColor(...)，或沿用组件默认的 padding，盖住下层、底色或内边距和源端不一致
适用范围：安卓控件没有自己的背景（未写或 @null），迁成 ArkUI 组件时
做法：
- 顺着父容器往上找第一个有 android:background 的那层；到布局根都没有，页面底色按 Activity 主题的 windowBackground 写
- 目标对应这一层不设背景或设 .backgroundColor(Color.Transparent)，底色只写在源端有背景的那一层；@null 去掉的还有背景带来的内边距，padding 按源端实际值四边写全
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- View 的内边距来自背景 drawable 的 getPadding；background=@null 时没有这部分内边距：源端去掉背景后，没写 padding 的边是 0（出处：android.view.View#setBackgroundDrawable）
- Stack 的子组件按顺序依次入栈，后一个子组件覆盖前一个子组件：叠在下层之上的组件设了不透明底色就会盖住下层（出处：ts-container-stack.md，页首说明）
- TextInput 默认 padding { top: 8vp, right: 16vp, bottom: 8vp, left: 16vp }：例：输入框不写 left 时起始边有 16vp 内边距（出处：ts-basic-components-textinput.md，属性说明）
针对本应用要查的：
- 透出来的底色：源工程布局 XML 里从这个控件往上各层父容器的 android:background；都没有时看 AndroidManifest.xml 里 Activity 或 application 的 android:theme，到 res/values 的主题文件里找 android:windowBackground；取到 @color/… 或 @drawable/… 再读出实际值，写在目标对应的那一层（通常是页面根容器）上；规格给的底色在源端查不到引用时登记差异
未核实：主题没写 windowBackground 时父主题里的默认值，族里的卡没查实
来源：3 张卡，3 个应用
- case-2a82c31c11fb4f1c7fa5（Blockinger）：做法第 1 步 ← 诊断
- case-5d12548f9d559985c27d（app_hnaccurateweather_live_android）：做法第 2 步 ← 建议 2
- case-85baa9234cc4f4798784（AntennaPod）：做法第 2 步 ← 建议 6

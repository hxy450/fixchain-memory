# 全屏页顶部避让：先找源端哪一层消费状态栏 inset，目标只在对应那一层加一次

审的是：代码
触发（任一种）：
- 读到：源布局的根、DrawerLayout、CoordinatorLayout 或 AppBarLayout 上有 android:fitsSystemWindows="true"，或工具栏容器自带固定 android:paddingTop 留白，或 Activity 的 setOnApplyWindowInsetsListener 只处理了部分边；写错的样子：目标的顶部避让（.padding({ top: … }) 或状态栏高度占位）落的层和源端消费 inset 的那一层对不上：不止一处、塞进固定 .height() 的标题栏、加在包住抽屉的容器上，或一处都没有
适用范围：Android 全屏页的状态栏避让由某一层布局或代码承担，迁成 ArkUI 页面接入顶部安全区时
做法：
- 在这一页的源布局和 Activity 里找出顶部 inset 由哪一层消费：带 android:fitsSystemWindows="true" 的那个 View、工具栏自带的 android:paddingTop，或 insets 监听里处理顶部的那一处；源端隐式消费的顶部也算
- 目标只在对应的那一层容器上加一次顶部避让值，其余层不再加；固定 .height() 的标题栏保持源高度，避让放在它外层
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- fitsSystemWindows 为 true 时调整这个 View 的 padding，给状态栏等系统窗口留出空间：源端顶部避让落在带这个属性的那一层，它里面的工具栏本身不缩（出处：Android SDK 平台资源 data/res/values/attrs.xml，fitsSystemWindows（按应用的 compileSdk 取对应平台））
- ArkUI 固定 .height() 包含 padding；安全区移到标题 Row 外层后，工具栏可见高度恢复为源高度：避让不要塞进固定高度的容器里（出处：卡里修好并验证过）
针对本应用要查的：
- 源端顶部 inset 由哪一层消费：源工程这一页的 Activity / Fragment 布局 XML：根布局、DrawerLayout、CoordinatorLayout、AppBarLayout 的 android:fitsSystemWindows，工具栏容器的 android:layout_height 和 android:paddingTop；以及 Activity 里的 setOnApplyWindowInsetsListener；按这一页的源布局从根往下逐层记下谁消费了顶部，不照搬别的页面；例：根布局 fitsSystemWindows="true"、工具栏固定 52dp 且没有 paddingTop 时，避让放在标题 Row 外层的容器上，Row 保持 52vp
来源：2 张卡，2 个应用
- case-7b7a48249f269a40a194（掌上燃气管家）：做法第 2 步 ← 建议 1、建议 4；取值 2 ← 诊断
- case-b4a2f2d65e01a68393e3（AntennaPod）：做法第 1 步 ← 建议 2

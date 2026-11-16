# 源 View 是 android:visibility="gone" 且代码没设为 VISIBLE 时，目标不渲染它

审的是：代码
触发（任一种）：
- 读到：布局 XML 里某个容器带 android:visibility="gone"，代码只改它子控件的 setText(...) / setVisibility(...)，没有对容器自身的 id 调 setVisibility(View.VISIBLE)；写错的样子：目标 build() 里无条件渲染这个容器，和别处同语义的标题、删除入口重复
- 读到：标题栏或工具栏的 ImageView 写着 android:visibility="gone"；代码里只有 findViewById 和 setOnClickListener，没有 setVisibility(View.VISIBLE)；写错的样子：目标标题栏上出现可点的 Image($r(...)) 入口加 onClick 跳转，照搬了目标工程其他页面的同类入口
适用范围：把带 gone / invisible View 的安卓布局和状态切换代码迁成 ArkUI 页面时，尤其参考的结构快照没有 visibility 属性时
做法：
- 逐个 View 从源布局 XML 取初始 android:visibility，再按它自身的 id 查所有 setVisibility 调用；初始 gone 且从不设为 VISIBLE 的就不渲染，或写 .visibility(Visibility.None)；目标工程别页的同类入口不作为它该显示的依据
- 按每种页面状态（如有数据、为空、结果、无结果）列出实际可见的标题和删除入口，确认同一语义只出现一次，并核对它们在哪个父容器里
- 源端靠左右对称让中间控件居中时，隐藏一侧放同尺寸的空占位（如和对侧返回键同大的 Row().width(<宽>).height(<高>)），不放可点图标
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- android:visibility 的取值：visible = 0（默认）、invisible = 1（不显示但占位）、gone = 2（完全隐藏，如同没有加入）：gone 的 View 不显示也不占位（出处：Android SDK 平台资源 data/res/values/attrs.xml，visibility（按应用的 compileSdk 取对应平台））
- View.GONE = 0x00000008：不可见，也不占布局空间：代码里没有改回 VISIBLE 时一直是这个状态（出处：android.view.View#GONE）
- visibility(value: Visibility): T：目标的可见性属性（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.visibility）
- Visibility.None：隐藏且不参与布局、不占位；Visibility.Hidden：隐藏但占位：gone 对应 None，invisible 对应 Hidden（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，Visibility）
- 把可点图标换回与对侧返回键同尺寸的空 Row，分段控件保持居中：卡里的修法（出处：卡里修好并验证过）
针对本应用要查的：
- 对侧控件的尺寸：源布局里标题栏对侧（如返回键）的 layout_width / layout_height，或目标页已写的对侧组件尺寸；空占位取同样的宽高
来源：2 张卡，2 个应用
- case-a348083ad18c6f87030f（刺猬猫阅读）：做法第 1 步 ← 建议 1、建议 3；做法第 3 步 ← 建议 2、诊断；取值 5 ← 诊断
- case-be590c45de6e4195a7aa（实时公交）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 2

# 源控件带 visibility 属性或被 setVisibility 时，先读初值和全部分支再写显隐

审的是：代码
触发（任一种）：
- 读到：布局 XML 里 android:visibility="gone" / "invisible"，或 Activity、Fragment、Adapter 代码里 setVisibility(View.GONE / View.VISIBLE / View.INVISIBLE)；写错的样子：目标无条件渲染、整块删掉，或几个控件包进一个共同 if；没按源端初值和各个条件写 if / .visibility(...)
适用范围：安卓控件的显隐迁成 ArkUI 的条件渲染或 visibility 属性时
做法：
- 从源布局 XML 取控件的 android:visibility 初值，再在 Activity / Fragment / Adapter 源码里按它自身的 id 搜全部 setVisibility 调用，记下每处的条件
- 从不置为可见的 gone 控件不渲染；有条件的逐个控件照条件写：View.GONE 写 if 不渲染或 .visibility(Visibility.None)，View.INVISIBLE 写 .visibility(Visibility.Hidden) 保留占位
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- visibility：visible = 0，invisible = 1（不显示但占位），gone = 2（完全隐藏，如同没加这个 View）：源端三个取值（出处：Android SDK 平台资源 data/res/values/attrs.xml，visibility（按应用的 compileSdk 取对应平台））
- visibility(value: Visibility): T：目标的可见性属性（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.visibility）
- Visibility.None：隐藏且不参与布局、不占位；Visibility.Hidden：隐藏但占位：gone 对应 None，invisible 对应 Hidden（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，Visibility）
针对本应用要查的：
- 控件的显隐初值和每个改变它的条件：源工程 res/layout 下布局 XML 里这个控件的 android:visibility；Activity、Fragment、Adapter 绑定方法里对它 id（R.id.… 或 binding 字段）的 setVisibility 调用；逐处读出 setVisibility 的参数和外面的 if 条件，原样搬成目标端 if 的条件或 .visibility 三元表达式的条件；同一行里几个控件条件不同的，各写各的
来源：2 张卡，2 个应用
- case-55bbad53c11b2d1b95e6（app_hnaccurateweather_live_android）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2
- case-be590c45de6e4195a7aa（实时公交）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1

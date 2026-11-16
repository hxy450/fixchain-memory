# 继承 View 的自定义控件上写了 android:checked 时，先核它是否被读取，初值取运行时生效值

审的是：代码
触发（任一种）：
- 读到：源布局的自定义控件（extends View implements Checkable，不是 CheckBox / CompoundButton）上声明 android:checked="true"，它的构造函数和 init(attrs) 只读自己的 styleable 属性，选中字段没有初值；show 之前没有调用 setChecked；写错的样子：目标端把首显状态写成 `@Local … : boolean = true`，注释只写「源 XML android:checked="true"」作依据
适用范围：界面实现阶段，把源布局里自定义控件的 XML 属性转成目标组件的初始状态时
做法：
- 转写前先查这个类的继承链和构造、init 实际读取的属性集合；没被读取的 android:* 属性运行时不起作用
- 初始状态取字段默认值（Java 的 boolean 字段没赋值即 false）和 show 之前代码里的 setChecked 调用
- 注释里分开写「XML 声明值」和「运行时生效值」，依据写到读取该属性或设置初值的那段代码，不只引用 XML
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- checked 定义在 CompoundButton、CheckedTextView 的 styleable 里：Indicates the initial checked state：android:checked 只由读取这些 styleable 的控件消费（出处：Android SDK 平台资源 data/res/values/attrs.xml，CompoundButton 的 checked（按应用的 compileSdk 取对应平台））
- a.getBoolean(com.android.internal.R.styleable.CompoundButton_checked, false); setChecked(checked);：CompoundButton 在构造里读 checked 并设初值；直接继承 View 的类没有这一步（出处：android.widget.CompoundButton#CompoundButton(Context, AttributeSet, int, int)）
- 改为首显未选中后与用户报告的源端行为一致：修好的做法（出处：卡里修好并验证过）
针对本应用要查的：
- 自定义控件的初始选中状态：源工程里这个自定义控件类的构造函数和 init(attrs)（看它 obtainStyledAttributes 读了哪些属性），以及弹窗或页面 show 之前的代码；构造里没读 checked、show 前也没有 setChecked 时，初值就是选中字段的默认值
未核实：首显未选中是按构造和 init 代码静态推断的，卡里没有安卓端真机记录
来源：1 张卡，1 个应用
- case-c1b719dc488b73e382db（免费来电多多）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1、诊断；做法第 3 步 ← 建议 2；取值 3 ← 诊断

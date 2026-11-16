# 带文字的 CheckBox/RadioButton 按源宽度定可点范围，折行的 layoutWeight 不扩命中区

审的是：代码
触发（任一种）：
- 读到：XML 里带 android:text 的 CheckBox / RadioButton，layout_width 为 wrap_content（无 layout_toLeftOf），或 match_parent、alignParentLeft + toLeftOf 两端锚定；写错的样子：wrap_content 项的 Text 写 .layoutWeight(1).onClick(...) 或整行 Row 挂 onClick；match_parent 项只有框和文字可点
- 读到：代码 new AppCompatCheckBox / AppCompatRadioButton、setText 后 addView 进 RadioGroup 或竖向 LinearLayout；写错的样子：RadioGroup 里的项整行可点，竖向 LinearLayout 里的项只有 Checkbox 方框可点
适用范围：带文字的 CheckBox / RadioButton 拆成 Checkbox / Radio 加 Text 时
做法：
- wrap_content 只让框和文字可点：内容宽容器（如 Flex 宽设 LayoutPolicy.wrapContent）挂 onClick；match_parent 或两端锚定才用整行 Row + onClick
- 代码创建的按父容器默认宽：RadioGroup.addView 为 WRAP_CONTENT，竖向 LinearLayout.addView 为 MATCH_PARENT；显式 setLayoutParams 以它为准
- 为折行加的 layoutWeight(1) 只管文字宽，不把 onClick 挂在这个撑满的 Text 上
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 竖向 LinearLayout 的默认 LayoutParams 是 (MATCH_PARENT, WRAP_CONTENT)：addView 没传 LayoutParams 时子项的宽（出处：android.widget.LinearLayout#generateDefaultLayoutParams）
- RadioGroup 的默认 LayoutParams 是 (WRAP_CONTENT, WRAP_CONTENT)：addView 进 RadioGroup 的单选项默认内容宽（出处：android.widget.RadioGroup#generateDefaultLayoutParams）
- LayoutPolicy.wrapContent：尺寸跟随子组件、但受父组件约束（@since 20）：内容宽容器的写法（出处：鸿蒙 SDK 的 ets/component/common.d.ts，LayoutPolicy.wrapContent）
- width(widthValue: Length | LayoutPolicy): T：宽可直接传 LayoutPolicy（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.width）
- 整行可点用整行 Row + onClick；内容宽用 Flex + LayoutPolicy.wrapContent，只框和文字可点；各处按源宽度选用：修好后的写法（出处：卡里修好并验证过）
- height(heightValue: Length | LayoutPolicy): T：同族接口：高同样可传 LayoutPolicy（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.height）
未核实：卡里的环境是 HarmonyOS SDK 6.1.1(24)，取值按本机 API 23 的声明核实
来源：1 张卡，1 个应用
- case-6d1435e3e9257286cfbf（MifareClassicTool）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 3；做法第 3 步 ← 建议 1；取值 5 ← 诊断

# 控件自身写了 textSize 时覆盖 style 默认值，目标逐控件取有效字号，不用 style 值统一代替

审的是：代码
触发（任一种）：
- 读到：按钮用 style 给默认 android:textSize，单个控件上又写了自己的 android:textSize（不同按键各不相同）；写错的样子：目标按键统一写 .fontSize(<style 默认值>)，丢了逐键的覆盖值
适用范围：源布局里控件既引用 style 又在自身写同名属性（textSize 等）时，迁成 ArkUI 组件
做法：
- 逐控件取有效属性：控件自身写的值优先于 style；先把每个按键的 textSize 列成表，再逐个写 .fontSize(n)（源 sp 数值直接写成 number，单位即 fp）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 属性取值的先后：AttributeSet 里控件自身写的值 → 它的 style → defStyleAttr / defStyleRes → 主题：控件上写的 textSize 覆盖 style 里的（出处：android.content.res.Resources.Theme#obtainStyledAttributes）
- fontSize(value: number | string | Resource): TextAttribute；number 的单位是 fp，默认 16fp：Text 的字号（出处：鸿蒙 SDK 的 ets/component/text.d.ts，TextAttribute.fontSize）
来源：1 张卡，1 个应用
- case-639b36918b1cd5c1bbe8（android-train-ticket-vest7）：做法第 1 步 ← 建议 1、诊断

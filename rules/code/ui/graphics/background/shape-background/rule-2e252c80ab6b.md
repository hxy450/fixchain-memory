# 源按钮自绘底色或渐变改成 SaveButton 时，底色和圆角设在 SaveButton 自身，不设透明底

审的是：代码
触发（任一种）：
- 读到：源按钮的 style 或背景 drawable 用 <gradient android:startColor / android:endColor>、<corners android:radius> 或半透明 <solid> 画底；派工或规格要求这个按钮改用 SaveButton 安全控件；写错的样子：SaveButton 上写 .backgroundColor(Color.Transparent)，底色、linearGradient 和 borderRadius 交给外层 Row / Column 容器，注释把「渐变容器承载 + 透明 SaveButton」定为范式
适用范围：用 SaveButton 等安全控件替代源端自绘外观（渐变、半透明胶囊、圆角描边）的按钮时
做法：
- 底色和圆角直接设在 SaveButton 上：.backgroundColor(源底色) .borderRadius(源 corners 的 radius)；源端是渐变的，用受支持的纯色近似（如取渐变主色）；外层容器最多只留描边和同值圆角
- 背景色的 alpha 不低于 0x1A，不写 Color.Transparent
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 安全控件背景色高八位 α 值低于 0x1a 时，系统强制调成 0xff；默认值 $r('sys.color.icon_emphasize')：Color.Transparent 会被压成不透明（真机上看到的是整面纯黑、圆角外露方角黑底）（出处：ts-securitycomponent-attributes.md，backgroundColor）
- backgroundColor(value: ResourceColor): T：安全控件自身的背景色（出处：鸿蒙 SDK 的 ets/component/security_component.d.ts，SecurityComponentMethod.backgroundColor）
- borderRadius(value: Dimension): T；borderRadius(radius: Dimension | BorderRadiuses): T（@since 15）：安全控件自身的圆角（出处：鸿蒙 SDK 的 ets/component/security_component.d.ts，SecurityComponentMethod.borderRadius）
- SecurityComponentMethod 里没有 linearGradient：渐变底只能用纯色近似（出处：鸿蒙 SDK 的 ets/component/security_component.d.ts，SecurityComponentMethod）
- declare class PasteButtonAttribute extends SecurityComponentMethod<PasteButtonAttribute>：同族接口：PasteButton 同样继承这套背景色和圆角，α 规则相同（出处：鸿蒙 SDK 的 ets/component/paste_button.d.ts，PasteButtonAttribute）
- 半透明底色和圆角改设在 SaveButton 自身后，按钮区均匀半透明，四角不再露黑：修复后保留的写法（出处：卡里修好并验证过）
针对本应用要查的：
- 源按钮的底色、渐变和圆角：源工程按钮 style 里 android:background 引用的 drawable（res/drawable 下的 shape XML）；读 <solid android:color> 或 <gradient> 的 startColor / endColor 取主色，<corners android:radius> 取 dp 数值；颜色若引用 @color，到 res/values/colors.xml 按名字找
未核实：卡里观察到的行为出自 API 24 目标 SDK，本机按 API 23 核实
来源：1 张卡，1 个应用
- case-affc8177e24ce9f71b47（免费来电多多）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 6 ← 诊断

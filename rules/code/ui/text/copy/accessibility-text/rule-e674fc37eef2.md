# 源图标 contentDescription 为 null 或空串时，不臆造无障碍文本，确需时用 $r 资源

审的是：代码
触发（任一种）：
- 读到：源端 Icon(…, contentDescription = null) 或 contentDescription = ""；写错的样子：目标给对应图标写死单一语言的 .accessibilityText('返回') 一类字面量，工程却是多语言资源
适用范围：转写图标的无障碍文本、工程有多语言字符串资源时
做法：
- 源端为 null 或空串时不写 accessibilityText；确需文本时写 .accessibilityText($r('app.string.<键>')) 并在各语言的 string.json 里补齐
- 写完搜 accessibilityText\('[^$] 一类字面量自检
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- accessibilityText(value: string): T 默认 ""；accessibilityText(text: Resource): T：有 Resource 重载，可按语言取资源（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.accessibilityText）
- 详情页、编辑页重写时移除写死的中文无障碍文本：修复后与源端一致（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-8dd5c1f1f269d142cc22（Cofi）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4；取值 2 ← 诊断

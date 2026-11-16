# 用命名尺寸资源承载源端 sp 值时，先读资源实际值再选名，注释与资源一致

审的是：代码
触发（任一种）：
- 读到：源布局写了具体字号 android:textSize="12sp"，或由主题、textAppearance 推出行标题字号（如 16sp）；写错的样子：代码用 fontSize($r('app.float.…')) 这类按名字挑的资源，注释写的 sp 数和该资源在 float.json 里的 value 不一样
适用范围：目标工程用 float.json 里的命名资源承载源端字号、尺寸数值时
做法：
- 引用前打开目标工程 resources/base/element/float.json，按 name 读出 value（如 "16.0fp"），只引用数值与源端相同的那一项
- 注释里写的数值必须和所引资源的 value 一致，不按 large、small、medium 这类名字猜数值
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- float 资源写在 element/float.json，每项 {"name": …, "value": "28.0fp"}，value 带单位：资源的实际数值只在 value 里，名字不代表数值（出处：resource-categories-and-access.md，资源文件示例）
- 按名字猜的数值与资源实际 value 不同（猜成 16 的实际更大），改成 value 与源端相同的资源后一致：名字和数值对不上是常态，必须读 value（出处：卡里修好并验证过）
针对本应用要查的：
- 所引命名资源的实际数值：目标工程 resources/base/element/float.json（及限定词目录下的同名文件），按 name 找；读 value 的数值和单位，与源端 sp 数比较；源端数值来自 dimens 的，在源工程 res/values/dimens.xml 里按 <dimen name> 读
来源：1 张卡，1 个应用
- case-85baa9234cc4f4798784（AntennaPod）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；取值 2 ← 诊断

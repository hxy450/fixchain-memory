# 按钮颜色资源按源端色值反查 color.json 里同值的键，不按 accent / primary 等名称挑

审的是：代码
触发（任一种）：
- 读到：源按钮的底色以色值字面量给出（如 app:shapeSolidColor="#AARRGGBB"、android:background 色值）；写错的样子：目标按钮写 .backgroundColor($r('app.color.…accent')) 这类按名称挑的键，而这个键在 color.json 里的值和源色值不同；高度、圆角、字色却都照抄了源
适用范围：目标工程已有颜色资源、其中有语义名相近但色值不同的键时，为按钮等控件选颜色资源
做法：
- 以源端实际色值（shapeSolidColor / background）在目标工程 color.json 里反查同值的键（不区分大小写比八位十六进制），引用它并核对所选键的值；不按 accent / primary 等名称推断
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- color.json 的标准值是八位十六进制，前两位透明度、后六位颜色：与安卓 #AARRGGBB 同序，源色值可直接逐字比对（出处：resource-categories-and-access.md，资源文件示例）
- Color.parseColor 支持 #RRGGBB、#AARRGGBB：源端色值的格式；六位的补 ff 透明度再比（出处：android.graphics.Color#parseColor）
- 改为与源色值同值的品牌色键后按钮颜色一致：修好的做法（出处：卡里修好并验证过）
针对本应用要查的：
- 与源色值同值的颜色键：目标工程 resources/base/element/color.json（及 dark 等限定词目录下的 color.json）；按 value 逐字比对（统一小写、补齐八位），取到的 name 写成 $r('app.color.<name>')；没有同值的键就新增一个
未核实：shapeSolidColor 出自第三方形状控件库，它的属性定义本机没有查
来源：1 张卡，1 个应用
- case-ae1e7b09c5cfe5214cd2（骑行记录）：做法第 1 步 ← 建议 3、诊断；取值 3 ← 诊断

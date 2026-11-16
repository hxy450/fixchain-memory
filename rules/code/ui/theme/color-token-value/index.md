# 颜色资源引用和源端色值

agent 会看到什么：源端颜色是字面量、@color/ 或 getColor(R.color.名)，目标工程已有一批颜色键；产物里 $r('app.color.…') 选了哪个键、'#…' 字面量从哪来

## 通用查法

### 目标引用颜色资源时，读出源端实际色值和 color.json 里键的 value 逐字比对再选键

审的是：代码
触发（任一种）：
- 读到：源端颜色是布局里的字面量（android:textColor="#…"、android:background、渐变起止色）、@color/ 引用或代码里的 getColor(R.color.名)；写错的样子：目标写 $r('app.color.X') 时按名称、前缀或色系挑了已有键，或照规格写了 '#…'，这个值和源端色值不同
适用范围：为目标控件选颜色资源引用或写颜色值时
做法：
- 读出源端这处的实际色值：字面量直接读，@color/ 或 R.color.名 到源工程 res/values 的 colors.xml 按 name 找；#RRGGBB 补 FF 成八位
- 到目标工程 resources/base/element 下的颜色 json 读候选键的 value，统一小写后和源色值逐字比；相等才引用，不等就用同值的键或新增专属键，不按名称、前缀或色系挑
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- #RRGGBB 解析时 alpha 置为 FF，与 #FFRRGGBB 相同：比对前把六位色值补成八位（出处：android.graphics.Color#parseColor）
- color.json 的颜色值是八位十六进制，前两位透明度、后六位颜色：与安卓 #AARRGGBB 同序，可以逐字比对（出处：resource-categories-and-access.md，资源文件示例）
针对本应用要查的：
- 源端这处的确切色值：源工程布局 XML 里该元素的颜色属性；写的是 @color/ 引用或代码里 getColor(R.color.名) 时，去 res/values 的 colors.xml 按 name 找；读出 #RRGGBB 或 #AARRGGBB，六位的补 FF 作透明度
- 候选颜色键的实际值：目标工程 resources/base/element（及 dark 等限定目录）下的 color.json 和各页共享的颜色文件，按 name 或按 value 找；读 value，统一小写、补齐八位后和源色值比
来源：3 张卡，3 个应用
- case-0cd1e854cf161b2bb256（掌上燃气管家）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1
- case-ae1e7b09c5cfe5214cd2（骑行记录）：做法第 2 步 ← 建议 3
- case-dfb696dc3a3684ce21d1（Blockinger）：做法第 1 步 ← 建议 4

## 规矩

- rule-8faf3b4bb73a｜复用已有 color token 前先比对它的值与源色值，不等就引用新增的专属键｜读到：源布局给元素写了字面色值（android:textColor="#…"、自定义属性里的渐变起止色），规格表也列出同一值；工程要求颜色一律 $r('app.color.*')、禁止 hex；写错：页面的 fontColor($r('app.color.X')) 或渐变色引用了同前缀、同色系的已有 token，而这个 token 的 value 与源色值不同；自检只统计到 hex 字面量为 0
- rule-4af9cc6eaf5e｜按钮颜色资源按源端色值反查 color.json 里同值的键，不按 accent / primary 等名称挑｜读到：源按钮的底色以色值字面量给出（如 app:shapeSolidColor="#AARRGGBB"、android:background 色值）；写错：目标按钮写 .backgroundColor($r('app.color.…accent')) 这类按名称挑的键，而这个键在 color.json 里的值和源色值不同；高度、圆角、字色却都照抄了源
- rule-8533a23e3bed｜源码按资源 ID 取色而规格给 hex 时，代码先对照 color.json 的同名键，不一致按源端资源写｜读到：安卓源码是 getColor(R.color.名) 或 getResources().getColor(R.color.名)，规格在同一处给的是 #hex；写错：代码里直接 return '#…' 字面量、注释只引规格条目，这个值和目标工程 resources/base/element/color.json 里同名 name 的 value 不一样
- rule-95c9f4530372｜代码里 Color.GREEN 等框架颜色常量按色值对令牌，没有同值令牌就新增｜读到：Java / Kotlin 里 setTextColor(Color.GREEN)、Color.RED 等 android.graphics.Color 常量；写错：目标对应处写 $r('app.color.…') 引用名字相近但色值不同的令牌（如淡绿），报告说是规格指定的令牌
- rule-a8c33990ce17｜把字面色值换成 $r('app.color.*') 时，引用条目的 value 要等于原色值，没有就先补｜读到：代码或源端里是字面色值（8 位 '#AARRGGBB' 串、Color(0xAARRGGBB)），工程要求颜色一律走 $r('app.color.*')，而 color.json 里没有同值的条目；写错：换成了名称相近或同为品牌色的已有令牌 $r('app.color.…')，它在 color.json 里的 value 和原色值不同
- rule-e37317d975b2｜源色值来自带深色覆盖的主题变量时，写 $r('app.color.*')，不写浅色 hex 字面量｜读到：源样式用 var(--ion-background-color)、var(--ion-text-color)、var(--ion-card-background) 或 Ionic 组件默认色，主题文件里这些变量有 body.dark 覆盖值；写错：页面写 .backgroundColor('#FFFFFF')、.fontColor('#000000')、Divider().color('#E0E0E0')，或 COLOR_BG 这类 string 常量存浅色 hex；也没有为这些中性色登记 FWD-REF

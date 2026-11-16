# 复用已有 color token 前先比对它的值与源色值，不等就引用新增的专属键

审的是：代码
触发（任一种）：
- 读到：源布局给元素写了字面色值（android:textColor="#…"、自定义属性里的渐变起止色），规格表也列出同一值；工程要求颜色一律 $r('app.color.*')、禁止 hex；写错的样子：页面的 fontColor($r('app.color.X')) 或渐变色引用了同前缀、同色系的已有 token，而这个 token 的 value 与源色值不同；自检只统计到 hex 字面量为 0
适用范围：界面转换时为元素选颜色资源引用，工程里已有同前缀或同色系的 token、也允许追加新键时
做法：
- 复用前读出 token 的实际 value，与源布局中这个元素的色值逐字比对（#RRGGBB 与 #FFRRGGBB 视为相等）；不相等就不复用，名称前缀相同、同属一个模块、同一色系都不算理由
- 没有等值资源时，按契约重读最新资源文件后追加页面或元素专属的颜色键，页面引用它；不为通过「无 hex」检查而改成值不同的已有 token
- 收口自检对本页每一处 $r('app.color.X') 解析出值，与源 XML 对应属性（textColor、渐变起止色等）逐项对账；不一致就修正，或报告 design_tokens_missing
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- #RRGGBB 解析时 alpha 置为 FF，与 #FFRRGGBB 相同：比对时忽略 alpha 前缀写法差异的依据（出处：android.graphics.Color#parseColor）
- 改引用值不同的已有 token 后颜色偏离源端；追加等值的专属键并引用后一致，共享 token 不动：修法（出处：卡里修好并验证过）
针对本应用要查的：
- 源端这个元素的确切色值：源工程布局 XML 里该元素的 android:textColor、背景或渐变属性；写的是 @color/ 引用时去 res/values 的 colors.xml 按 name 找；读出 #RRGGBB 或 #AARRGGBB，前者补 FF 作 alpha
- 候选 token 的实际值：目标工程 resources/base/element 下各个颜色 json（含各页共享的颜色文件），按 name 找；读 value，与源色值逐字比对
来源：1 张卡，1 个应用
- case-0cd1e854cf161b2bb256（掌上燃气管家）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 2、诊断；做法第 3 步 ← 建议 3；取值 2 ← 诊断

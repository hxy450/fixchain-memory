# 判定图标资源未迁移前，查 base 和各密度限定目录并按源端实际 drawable 名核对

审的是：代码
触发（任一种）：
- 读到：源端 setImageResource(R.drawable.…) 或布局 XML 的 android:src 指向某个 drawable；写错的样子：代码注释写「某资产未迁移」，回落到别的图标（$r('app.media.…') 换成普通态图标），判断依据只是看了 resources/base/media
适用范围：目标代码按状态切换图标、怀疑某个资源没迁过来时
做法：
- 先按源端设置图标的代码（setImageResource、布局 XML）确认实际 drawable 名，再在 resources/base/media 和 ldpi、mdpi、xldpi、xxldpi、xxxldpi 等密度限定目录的 media 下找同名文件
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 系统先在与设备状态匹配的限定词目录里找资源，找不到或没有匹配的限定词目录时才去 base 目录：资源可能只在限定目录里，只看 base 会误判（出处：resource-categories-and-access.md，资源匹配）
- 屏幕密度限定词：sdpi、mdpi、ldpi、xldpi、xxldpi、xxxldpi（xxxldpi 适用于 dpi 在 (480, 640] 的设备）：要查的密度目录（出处：resource-categories-and-access.md，限定词目录）
- 改用源端实际的两个 drawable 后，全景快门态和取消按钮与源端一致：按源端实际资源名接线（出处：卡里修好并验证过）
针对本应用要查的：
- 源端这个状态用的 drawable 名：源工程设置该图标的 Java/Kotlin 代码（setImageResource）和布局 XML 的 android:src；取 R.drawable 后的名字，到目标 resources 各 media 目录找同名文件
未核实：只放在密度限定目录、base 下没有同名文件的 media 资源能否被 $r 正常解析，卡里没核实
来源：1 张卡，1 个应用
- case-4171cd43bbb420b4ee40（opencamera-hmos）：做法第 1 步 ← 建议 4；取值 3 ← 诊断

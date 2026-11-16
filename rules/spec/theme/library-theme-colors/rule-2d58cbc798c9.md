# 规格写“页面零硬编码色值”时，同句写明要用 $r('app.color.…') 引用语义色

审的是：规格
触发（任一种）：
- 读到：源端颜色来自主题语义色（colorPrimary、colorOnPrimary 等），深浅色分 values / values-night 两套；写错的样子：规格或功能规格写“页面代码零硬编码色值”“主题深浅色 out of scope”，没写允许并要求用 $r('app.color.…') 引用已迁移的语义色
适用范围：规格里写颜色约束（零硬编码、深浅色交给资源系统）的那一句
做法：
- 在这条约束后补一句：页面上需要的颜色一律写 $r('app.color.<语义色名>') 引用已迁移的资源，深浅色由 base / dark 两套资源自动切换；零硬编码不是不设颜色属性
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 颜色模式限定词：dark（深色模式）、light（浅色模式）：dark 目录下的同名颜色资源在深色模式下自动替换 base 的值（出处：resource-categories-and-access.md，限定词目录）
- .fontColor($r('app.color.…'))、.backgroundColor($r('app.color.…'))：页面里引用本模块颜色资源的写法（出处：resource-categories-and-access.md，访问本模块资源或模块依赖的HAR资源）
- 只写“零硬编码色值”时，实现者把它读成不得设置颜色属性，按钮落回平台默认色：误读的后果（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-97a40a9d2dce65dc9f9c（Dice Roller）：做法第 1 步 ← 建议 2、诊断；取值 3 ← 诊断

# 源端由调用方 Modifier.size 给图片子组件定尺寸时，目标在槽外层或调用处写 .width/.height

审的是：代码
触发（任一种）：
- 读到：Compose 调用方把 Modifier.size(...) 当作 modifier 参数传给图片子组件，有图和无图分支共用同一个尺寸修饰符；被嵌的图片组件自身没有尺寸参数；写错的样子：拆成 @Builder 槽或接线调用被嵌组件后，有图分支的槽外层容器和调用处都没有 .width(...)/.height(...)，只有占位分支写了尺寸；FWD-REF 注释里也没写尺寸
- 读到：Row 里一列带 Modifier.weight(1)，旁边是固定尺寸的图片；写错的样子：Row { Column().layoutWeight(1) ; Image(...) } 里不带 layoutWeight 的 Image 或图片组件没有 .width/.height，权重列被挤成 0 宽
适用范围：Compose 里尺寸由调用方 Modifier 传给图片子组件、或 Row 里权重列旁边放图片，迁成 ArkUI 时
做法：
- 把源端 Modifier.size(X) 的 X（dp 数值写成同值 vp）写在 @Builder 槽的外层容器或槽调用处：.width(X).height(X)；被嵌组件没有尺寸参数时在调用处补 .width/.height，有图、无图分支都要有
- 写完 Row { 某列.layoutWeight(1) ; … } 后，逐个确认不带 layoutWeight 的同级子项有确定的 width/height，网络图片尤其要写
- 槽的 FWD-REF 注释里写明尺寸，接线者按它在调用处补尺寸
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- layoutWeight(value: number | string): T：不设 layoutWeight（或为 0）的子项先按自身尺寸占位，剩下的主轴空间才按权重分给权重子项；非权重子项没有确定尺寸就会占掉剩余空间（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.layoutWeight；ts-universal-attributes-size.md，layoutWeight）
- Image 加载成功且不设宽高时，显示大小自适应父组件：图片组件不写 .width/.height 时尺寸不受源端定尺寸约束（出处：ts-basic-components-image.md，接口）
- width(value: Length): T；height(value: Length): T：在槽外层容器或调用处定尺寸用的通用属性（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.width / CommonMethod.height）
- 有图分支不设尺寸时，图片在 Row 中抢走全部宽度、标题列被挤成 0 宽；改为图片固定尺寸、标题列 layoutWeight(1) 后恢复：缺尺寸的后果和修法（出处：卡里修好并验证过）
针对本应用要查的：
- 调用方给图片子组件的尺寸值：源工程 Compose 文件里调用该图片子组件处的 Modifier.size(...) 参数，及它引用的尺寸常量定义；读出 dp 数值，目标写成同值 vp 的 .width/.height
未核实：卡里观察到的行为出自鸿蒙 SDK API 24（6.1.1），本机核实用 API 23
来源：1 张卡，1 个应用
- case-bcc79fa7d3d15ef4a8b2（jerboa）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2；做法第 3 步 ← 建议 1；取值 4 ← 诊断

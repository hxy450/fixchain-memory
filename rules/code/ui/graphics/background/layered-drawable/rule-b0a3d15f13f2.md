# 位图资产暂缺、编译在补资源后才跑时，照常写 Image($r('app.media.…')) 引用，不降成注释

审的是：代码
触发（任一种）：
- 读到：规格或转换决策写了全屏 Image 背景或位图层，源端引用 @mipmap/、@drawable/ 位图，而目标 resources/base/media 下还没有这张图；写错的样子：该处没有 Image(...)，只留 `FWD-REF` 注释（带 P-RES-ASSET- 编号）和「资产未迁移，就绪后补 Image 层」一类散文，或用 .backgroundColor(...) 顶替位图层
适用范围：界面转换阶段位图还没进目标 media、而编译在批次收尾补资源之后才跑时
做法：
- 照常写 Image($r('app.media.<源位图名>')) 和它的几何，资源名取源位图名；在转换报告里申报缺的资产（源 sourceSet 里的位置 → 目标 resources/base/media）
- 或者直接从源 sourceSet（含 flavor 目录）把位图拷进目标 resources/base/media 再引用
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- $r('app.type.name')，media 类资源写 $r('app.media.<文件名>')：引用本模块 media 目录里的图片（出处：resource-categories-and-access.md，资源访问）
- declare function $r(value: string, ...params: any[]): Resource：$r 的参数格式是 'belonging.type.name'（出处：鸿蒙 SDK 的 ets/component/common.d.ts，$r）
- media 目录支持 .jpg、.png、.gif、.svg、.webp、.bmp：源端的 webp、png 位图可以原样拷进 base/media（出处：resource-categories-and-access.md，资源组目录（表3 图片资源类型说明））
- 两张位图拷进 base/media 后，Stack 首层 Image 引用即可显示，去掉 FWD-REF：修好后的写法（出处：卡里修好并验证过）
针对本应用要查的：
- 缺的位图在源工程的位置：源工程对应 sourceSet（main 或生效 flavor）的 res/mipmap-*、res/drawable-* 下按资源名找；取到文件后写进转换报告的缺口清单，或直接拷进目标 resources/base/media
未核实：卡里上机看到的行为出自 HarmonyOS API 21/24，本机声明按 API 23 核实
来源：1 张卡，1 个应用
- case-bcb4b234c7b3327e2100（DeepAI全能PPT）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2；取值 4 ← 诊断

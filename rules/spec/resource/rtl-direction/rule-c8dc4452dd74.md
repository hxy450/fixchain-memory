# 规格把 Canvas.drawText 映射到 fillText 时，写出按首个强方向字符设 direction 的契约

审的是：规格
触发（任一种）：
- 读到：源端用 `Canvas.drawText(..., paint)` 配默认 `new Paint()` 画文字，没做 bidi 或方向设置；资源里有 values-fa 等 RTL 语言；写错的样子：规格映射写「drawText→fillText 1:1 移植」，或写「按原串绘制即 parity、不需特殊 RTL 处理」「Android drawText 同样不做 bidi」，没有段落方向契约
适用范围：规格提取阶段，安卓 Canvas 文字迁到 ArkUI Canvas fillText 的映射行
做法：
- 映射里写明：安卓默认 Paint 的 bidi 是 BIDI_DEFAULT_LTR，每串按首个强方向字符定段落方向，无强字符时 LTR，与系统语言无关；ArkUI 画布 direction 默认 inherit，跟随画布组件和系统语言
- 契约要求每次 fillText 前按该串首个强方向字符设 ctx.direction（'rtl' 或 'ltr'），不写「1:1 移植、不需特殊 RTL 处理」
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- mBidiFlags = BIDI_DEFAULT_LTR：Paint 的 bidi 初值：按启发式判段落方向，判不出时 LTR（出处：android.graphics.Paint 的 mBidiFlags、BIDI_DEFAULT_LTR）
- nDrawText(..., paint.mBidiFlags, ...)：Canvas.drawText 把 Paint 的 bidi 标志交给绘制，所以安卓 drawText 是做 bidi 的（出处：android.graphics.BaseCanvas#drawText）
- direction: CanvasDirection，@default inherit；CanvasDirection = "inherit" | "ltr" | "rtl"：画布文字方向，默认继承画布组件的设置（出处：鸿蒙 SDK 的 ets/component/canvas.d.ts，CanvasRenderer.direction、CanvasDirection）
来源：1 张卡，1 个应用
- case-e485c29b5b8cabfc9f01（2048）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1

# Paint 字号按 scaledDensity 算时，Canvas font 用 fp2px 换成 px 并带 bold

审的是：代码
触发（任一种）：
- 读到：源端 Paint.setTextSize(N * scaledDensity + 0.5f)（sp 字号），Paint.setTypeface(Typeface.create(Typeface.DEFAULT, Typeface.BOLD))；写错的样子：目标端 ctx.font 写成固定的 '14px sans-serif' 这类：sp 数值直接当 px，没有按 fp 换算，也丢了 bold
适用范围：把安卓 Canvas+Paint 的文字绘制迁成 ArkUI CanvasRenderingContext2D（默认构造、vp 坐标）时的 font 字符串
做法：
- 写成 ctx.font = `bold ${fp2px(N) + 0.5}px sans-serif`：font 串里的 px 是物理像素，sp 字号 N 先经 fp2px 换成 px；源端 Typeface 是 BOLD 时带上 bold；不要假设 'Npx' 在 vp 画布里按 vp 解释
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- font 语法 'font-style font-weight font-size font-family'；font-size 单位支持 px、vp，使用时要加单位；默认 'normal normal 14px sans-serif'：字号单位写在字符串里（出处：ts-canvasrenderingcontext2d.md，font）
- px：屏幕物理像素单位；fp：字体像素，随屏幕密度和系统字体大小设置变化：sp 对应 fp，写进 font 串前要换成 px（出处：ts-pixel-units.md，基本像素单位）
- declare function fp2px(value: number): number，@deprecated since 18，@useinstead UIContext#fp2px：把 fp 数值换成 px（出处：鸿蒙 SDK 的 ets/component/common.d.ts，fp2px）
- Paint.setTextSize(float textSize) 的 textSize 是像素：源端 N * scaledDensity 算出的是物理像素（出处：android.graphics.Paint#setTextSize）
- DisplayMetrics.scaledDensity：字体缩放系数，同 density，但会按用户字体大小偏好调整：N * scaledDensity 是 sp 换 px，目标端对应 fp 换 px（出处：android.util.DisplayMetrics#scaledDensity）
- setFont 改为 bold ${fp2px(fp)+0.5}px 后字号随密度和字体缩放，和源端一致：验证过的字号写法（出处：卡里修好并验证过）
未核实：卡里环境是 HarmonyOS 6.1.1（API 24），本机声明是 API 23
来源：1 张卡，1 个应用
- case-0543bbad1d6bc5c2cfde（opencamera-hmos）：做法第 1 步 ← 建议 1、诊断；取值 6 ← 诊断

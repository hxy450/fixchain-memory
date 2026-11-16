# 规格里自定义字体的 Canvas font 串只写字号和注册字族名，不加引号、不叠加 bold

审的是：规格
触发（任一种）：
- 读到：源端 Typeface.createFromAsset(...) 装载单一字面的字体文件后直接 paint.setTypeface(...)，没有另外请求 Typeface.BOLD 或 ITALIC；写错的样子：规格规定 Canvas 文本统一 font: "bold <size>px '字族名'"：字族名带引号，还加了源端没有的 bold
适用范围：规格为源端自定义字体制定 ArkUI Canvas 的 ctx.font 格式时；Canvas font 引用注册的自定义字体自 API 20 起支持（出自文档）
做法：
- font 串格式写成 `${size}px <注册字族名>`：字族名不加引号；源端没请求 bold/italic 的不写；单一字面的字体文件（例如本身就是粗体的文件）按 normal 引用
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- ctx.font = 'font-style font-weight font-size font-family'，各项可选，font-size 要带单位 px 或 vp：Canvas font 串的语法（出处：ts-canvasrenderingcontext2d.md，font）
- font: string，默认 normal normal 14px sans-serif：CanvasRenderer 的 font 属性，CanvasRenderingContext2D 和 OffscreenCanvasRenderingContext2D 共用（出处：鸿蒙 SDK 的 ets/component/canvas.d.ts，CanvasRenderer.font）
- this.context.font = "bold 30vp HarmonyOS_Sans_Thin_Italic"：文档示例里自定义字族名不加引号（出处：ts-canvasrenderingcontext2d.md，font）
- 字族名带引号时无论是否 bold，首次布局都回落系统字体；去掉引号、normal 字重后首次布局得到注册字体的度量：规格格式的依据（出处：卡里修好并验证过）
针对本应用要查的：
- 注册字族名和源端请求的字重、字形：源工程里 Typeface.createFromAsset / Typeface.create 的调用和字体文件名；目标工程 registerFont 的 familyName；font 串里的字族名与 familyName 逐字一致；源端只有 createFromAsset、没有 Typeface.create(…, Typeface.BOLD) 的，不写 bold
来源：1 张卡，1 个应用
- case-6c0506e04f18067f4274（2048）：做法第 1 步 ← 建议 1、诊断；取值 4 ← 诊断

# Canvas 用注册字体时 ctx.font 写 `${size}px 字族名`，不加引号、不加源端没有的 bold

审的是：代码
触发（任一种）：
- 读到：源端 Typeface.createFromAsset(...) 后 paint.setTypeface(...)，没有额外的 Typeface.BOLD；写错的样子：目标端 ctx.font 组装成 `bold ${size}px '${字族名}'`：字族名外包了单引号，或多了源端没有的 bold
适用范围：ArkUI Canvas 用 registerFont 注册的自定义字体绘制和 measureText 时
做法：
- 写成 ctx.font = `${size}px ${familyName}`：familyName 与 registerFont({ familyName, familySrc }) 里的完全一致、不加引号；源端没请求粗体的不写 bold，单一字面的字体文件按 normal 引用
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- registerFont(options: font.FontOptions): void；FontOptions { familyName: string | Resource; familySrc: string | Resource }：UIContext.getFont() 上的注册接口，familyName 就是 font 串里要写的字族名（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，Font.registerFont；ets/api/@ohos.font.d.ts，FontOptions）
- font.registerFont 自 API 18 起废弃，改用 UIContext.Font#registerFont：新代码从 this.getUIContext().getFont() 取注册接口（出处：鸿蒙 SDK 的 ets/api/@ohos.font.d.ts，font.registerFont）
- this.context.font = "bold 30vp HarmonyOS_Sans_Thin_Italic"：文档示例里自定义字族名不加引号（出处：ts-canvasrenderingcontext2d.md，font）
- canvasFont 改成 `${size}px <字族名>`（无引号、normal 字重）后，冷启首次布局得到注册字体的度量：改法的依据（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-6c0506e04f18067f4274（2048）：做法第 1 步 ← 建议 1、诊断；取值 4 ← 诊断

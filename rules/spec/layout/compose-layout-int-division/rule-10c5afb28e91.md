# Compose Layout 对 constraints 整除或 .toInt() 时，规格写明在 px 域算

审的是：规格
触发（任一种）：
- 读到：Compose 自定义 Layout / MeasureScope 里在 constraints.maxWidth、placeable 宽高上做 Kotlin Int 整除或 .toInt() 截断（如 constraints.maxWidth / (itemCount + 1)）；写错的样子：规格把这条公式写成 vp 域整除（W 标「vp，整数」、注释对应 constraints.maxWidth，u = floor(W/(n+1))），把 onAreaChange 的回调宽写成「vp，整数」，映射表写「measureText 返回 px，须 px2vp 后进入 vp 域公式」
适用范围：规格提取阶段把 Compose 自定义布局里的整数几何公式翻译成目标公式、标注运算单位时
做法：
- 规格写明：constraints、placeable 的宽高是 Int px，整除和 .toInt() 发生在 px 域；目标公式同样在 px 域算——onAreaChange 的 vp 宽先 vp2px，measureText 的 px 结果直接进公式，结果写进 .width / .translate / .position 前再 px2vp
- onAreaChange 的回调宽写成「vp，浮点」，不写「vp，整数」；源码里本来就是 Dp 的常量仍按 vp 写
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Area.width：目标元素的宽度，单位 vp：onAreaChange 回调里 newValue.width 是 vp，不是整数（出处：ts-types.md，Area）
- measureText(options: MeasureOptions): number，返回值单位 px：测出的文字宽是 px，可直接进 px 域公式（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，MeasureUtils.measureText）
- vp2px(value: number): number、px2vp(value: number): number：进出 px 域的换算（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，UIContext.vp2px / UIContext.px2vp）
- 改成 px 域 floor / trunc 后，Row 总宽等于容器 px 宽、各槽宽与源端一致；vp 域 floor 时右侧留出余量、整体左偏：两种运算域的实测差别（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-0ff695bbe2304e899b77（Jetsnack）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1、诊断；取值 4 ← 诊断

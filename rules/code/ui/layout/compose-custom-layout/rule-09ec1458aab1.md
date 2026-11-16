# 源端 px 域整除公式落成纯函数时，参数带 Px，调用处 vp2px → 公式 → px2vp

审的是：代码
触发（任一种）：
- 读到：Compose Layout 里的 constraints.maxWidth / (itemCount + 1)，以及 placeable 位置上的 .toInt()；写错的样子：Math.floor(w / (n + 1)) / Math.trunc(...) 的输入是 onAreaChange 回写的 vp 宽，measureText 的 px 结果先 px2vp 再进公式，头注释写「All lengths are vp」
适用范围：把源端 Compose 布局里的整数几何公式落成 ArkTS 纯函数，并用 onAreaChange / measureText 的返回值喂它时
做法：
- 纯函数的参数名写明单位（如 widthPx、labelWidthsPx），算法照源端在 px 域 Math.floor / Math.trunc，头注释写调用方必须传 px
- 调用处：onAreaChange 的 newValue.width 经 uiContext.vp2px(...) 存成 px，measureText 的结果保持 px，公式输出写进 .width / .translate / .position 前 uiContext.px2vp(...)
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- vp2px(value: number): number：onAreaChange 的 vp 宽换成 px（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，UIContext.vp2px）
- px2vp(value: number): number：px 域结果写回组件属性前换回 vp（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，UIContext.px2vp）
- measureText(options: MeasureOptions): number，返回值单位 px：文字宽直接是 px，不先 px2vp（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，MeasureUtils.measureText）
- Area.width：目标元素的宽度，单位 vp：onAreaChange 回调的宽是 vp 浮点（出处：ts-types.md，Area）
- 宽度、文字宽、槽宽、指示器位置、图标位置全部在 px 域 floor / trunc，写入属性前 px2vp 后，Row 铺满容器、图标中心与源端一致；vp 域 trunc 还会额外丢掉小数 vp：修复后的形态（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-0ff695bbe2304e899b77（Jetsnack）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3、诊断；取值 5 ← 诊断

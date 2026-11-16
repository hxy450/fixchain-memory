# bindSheet FIT_CONTENT 弹层里可能超高的 Scroll 要写非 None 的 edgeEffect

审的是：代码
触发（任一种）：
- 读到：源端 ModalBottomSheet(skipPartiallyExpanded = true) 的内容是 Column(Modifier.verticalScroll(...))，长列表、横屏或大字号时会超过弹层高度；写错的样子：宿主 bindSheet(…, { height: SheetSize.FIT_CONTENT }) 的内容写成 Scroll{Column}，Scroll 修饰链只有 width、backgroundColor、scrollBar，没有 .edgeEffect(...)；注释写「按内容定高、到上限后就滚动」
适用范围：bindSheet 半模态高度用 SheetSize.FIT_CONTENT、内容区是 Scroll 且内容可能超过弹层上限时
做法：
- 内容区 Scroll 写 .edgeEffect(EdgeEffect.Spring, { alwaysEnabled: false })；Scroll、Column 照旧不写 height('100%')，由弹层上限约束
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- FIT_CONTENT 半模态里 edgeEffect 为默认 None 的内容 Scroll 超过上限后不响应拖动；只补 .edgeEffect(EdgeEffect.Spring, { alwaysEnabled: false }) 就能滚到底：上机看到的行为，声明和文档里没写（出处：卡里修好并验证过）
- bindSheet(isShow: boolean, builder: CustomBuilder, options?: SheetOptions): T：半模态的绑定方法（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.bindSheet）
- SheetSize.FIT_CONTENT = 2：弹层高度随内容自适应，@since 12：触发这个问题的高度档（出处：鸿蒙 SDK 的 ets/component/common.d.ts，SheetSize.FIT_CONTENT）
- edgeEffect(edgeEffect: EdgeEffect, options?: EdgeEffectOptions): ScrollAttribute；默认 EdgeEffect.None：Scroll 不写时就是 None（出处：鸿蒙 SDK 的 ets/component/scroll.d.ts，ScrollAttribute.edgeEffect）
未核实：只在 HarmonyOS 6.1.0 设备上两处 FIT_CONTENT 弹层实测过；其他高度档、非半模态里的 Scroll 是否同样拖不动没有核实
来源：1 张卡，1 个应用
- case-cdc263993782c99990b7（GameOfLife）：做法第 1 步 ← 诊断；取值 1 ← 诊断

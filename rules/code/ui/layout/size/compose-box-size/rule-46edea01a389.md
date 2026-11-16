# 没有显式宽高的容器不直接写 .border()，改用按测得尺寸定位的覆盖层画描边

审的是：代码
触发（任一种）：
- 读到：源组件用 Compose Modifier.border(BorderStroke, shape) 在已定尺的盒内侧描边；写错的样子：目标在没有 width / height、尺寸由内容决定的 Stack 或 Column 上直接写 .border(...)
适用范围：界面实现阶段，给尺寸由内容决定的容器加描边时
做法：
- 去掉容器上的 .border()；容器用 .onSizeChange 记下宽高，描边非空时在容器内追加覆盖层 Column().width(测得宽).height(测得高).position({ x: 0, y: 0 }).border(描边参数).hitTestBehavior(HitTestMode.None)
- 写 .border() 前先查这个节点有没有显式 width / height；有就照常写，没有就用上一步的覆盖层，并在注释里写明「内容盒 = 描边盒」的预期
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- border(value: BorderOptions): T：组件边框，声明里没写尺寸语义（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.border）
- onSizeChange(event: SizeChangeCallback): T：组件尺寸变化时拿到新宽高，给覆盖层定尺（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onSizeChange）
- position(value: Position | Edges | LocalizedEdges): T：覆盖层绝对定位到容器左上角（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.position）
- hitTestBehavior(value: HitTestMode): T；HitTestMode.None 自身不响应触摸：覆盖层不拦截点击（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.hitTestBehavior；ets/component/enums.d.ts，HitTestMode.None）
- 改成覆盖层后盒尺寸与 Android 一致，代价是首帧还没测到尺寸时缺描边：修复后保留的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-77c4d0c99ad4a6486b79（Jetsnack）：做法第 1 步 ← 诊断；做法第 2 步 ← 建议 2；取值 5 ← 诊断

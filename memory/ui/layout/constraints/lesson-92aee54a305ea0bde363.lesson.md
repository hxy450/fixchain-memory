# Stack 中内容尺寸的子项按 alignContent 定位：子项自身的 .align() 不改变它在父容器中的位置，需要的对齐用满尺寸容器或显式 position

ID：`lesson-92aee54a305ea0bde363` · 版本：7

[本主题](index.md)

## 何时使用

界面转换与巡检修复阶段，把 Compose 自定义 Layout 或 Box 中的文字改写为 ArkUI Stack 子节点并确定纵向位置时；修复或编译清理删除 height('100%')、.align() 等居中手段时；把 FrameLayout 中按 layout_gravity 叠放的角标、重叠头像翻译成 Stack 时；把 Compose Box 中以 Modifier.align(BottomCenter 等) 定位的子项翻成 Stack 子节点时；把 FrameLayout/CoordinatorLayout 的 layout_gravity、RelativeLayout 的 alignParent*/centerInParent 翻译为 Stack 中 FAB、多选浮层、工具栏、装饰条的定位并确定叠层次序时；把 ConstraintLayout 标题栏（左返回、居中标题、右侧操作）转换为 ArkUI 或抽取公共标题栏组件时

## 适用情境

源端自定义 Layout 用 placeRelative(x, (maxHeight - height) / 2) 把定宽文字纵向居中，或 Box 中文字按居中对齐放置；目标用 Stack({ alignContent: Alignment.TopStart }) 同时容纳文字与图片等对齐需求不同的子项。也包括源端固定尺寸 FrameLayout 中的小角标以 layout_gravity=end|bottom 贴右下，目标写成 Stack({ alignContent: Alignment.TopStart }) 并只给角标加 .align(Alignment.BottomEnd)。也包括源 Box 中部分子项用 Modifier.align 放到非默认位置（如贴底的购买栏），目标 Stack 设了统一的 alignContent(TopStart)，规格写着“底部对齐”。也包括映射参考或兄弟页把 layout_gravity 写成 .align(Alignment.X)，工具栏、浮层、FAB 于是落在父 Stack 中部。也包括标题栏：返回图标约束到父 start、右侧入口约束到 end、标题 0dp 加左右 margin 居中，目标写成 Stack({ alignContent: Alignment.Center }) 并只给返回图标加 .align(Alignment.Start)，后写的页面与公共标题栏组件以它为模板复制。

## 原因

Stack 按 alignContent 放置未撑满的子节点；Text 的 .align() 只对齐文字在自身框内的位置，内容高的 Text 在 TopStart 的 Stack 里仍落在左上角，ArkUI Alignment 也没有 Compose 的 CenterStart。来源中巡检修复者为裁剪图片把 Row 改成 TopStart 的 Stack，删去 Text 的满高后改写 .align(Alignment.CenterStart) 并自称已居中；编译修复把它改成 Alignment.Start，随后又被删除，分类卡文字一直贴左上。另一应用的成员头像角标照此写成子项 .align(BottomEnd)，角标仍在左上；该片段后来被抽进共享组件继续沿用，直到改成 position 才贴到右下。

## 做法

1. 同一 Stack 中各子项对齐需求不同时，给文字包一个满高容器：Column().width(源端比例).height('100%').justifyContent(FlexAlign.Center).alignItems(HorizontalAlign.Start)，或给子项按源公式单独 position/offset。
2. 删除 height('100%')、.align() 等手段前，确认替代约束仍实现原来的纵向位置；枚举名以 ArkUI SDK 为准，不照搬 Compose 的 Alignment 名称。
3. 按 layout_gravity 单独对齐某个子项（如 end|bottom 的角标）时，在已知 W×H 的容器里写 position({ x: W - 子宽, y: H - 子高 })，或给该子项单独套一个 alignContent 为对应方向的 Stack。
4. 逐个核对源 Box 子项的 Modifier.align：非默认位置写成 position({ left: 0, bottom: 0 })、markAnchor 等实际属性；规格或报告里的“底部对齐”要落到代码属性上。
5. 子项单向贴边时可改父 Stack({ alignContent })；同一 Stack 内混合对齐用 .position({ left/right/top/bottom })、markAnchor 或满幅透明容器配 justifyContent/alignItems，并保留源 margin。
6. 叠层按源布局声明顺序复核 z 序（后声明者在上），无法按序排列时补 zIndex。
7. 标题栏按约束建互斥的水平槽位：Row 内左侧固定宽槽（宽取标题的 marginStart）放返回入口，layoutWeight(1) 的标题居中，右侧固定槽放操作入口；也可用 RelativeContainer + alignRules 对应 start/end 约束。

## 可选检查

- 沿用了映射参考或先例中的定位写法时，检索 .align(Alignment.，逐个确认它要的是内容对齐还是在父容器中的位置
- 标题栏同时打开返回与右侧入口并用较长标题预览，确认三者不重叠、标题在两侧槽位之间居中

来源支持：9 张卡 · 6 次迁移 · 5 个应用

## 来源（按需复核）

- [case-4f627840679361f165a3](../../../../store/cases/case-4f627840679361f165a3/8b0f7cc40d821777a77dc3bf68c6739f335039023414e9bcb04404d5b4ac02e8.json) · 结论：recommendation:2
  卡片版本：`8b0f7cc40d821777a77dc3bf68c6739f335039023414e9bcb04404d5b4ac02e8`
- [case-5e35bb283520acf3bd35](../../../../store/cases/case-5e35bb283520acf3bd35/954c420a6eb53234d9a40e9851863e13e6a2b9e3e2195abc6f71fcfe048dcf4f.json) · 结论：recommendation:3
  卡片版本：`954c420a6eb53234d9a40e9851863e13e6a2b9e3e2195abc6f71fcfe048dcf4f`
- [case-83dafcc0eaba740bd9c0](../../../../store/cases/case-83dafcc0eaba740bd9c0/63799a14d87533825a0449dd85653c66535fbb31296be482c5feada55b5522a6.json) · 结论：diagnosis, recommendation:1
  卡片版本：`63799a14d87533825a0449dd85653c66535fbb31296be482c5feada55b5522a6`
- [case-9058ac868b6feb3a04e0](../../../../store/cases/case-9058ac868b6feb3a04e0/d8e013afe2706da7f1b19c1a0d603c05f971b4ebc0c4542f6fb5e8a956b3ebc4.json) · 结论：recommendation:4
  卡片版本：`d8e013afe2706da7f1b19c1a0d603c05f971b4ebc0c4542f6fb5e8a956b3ebc4`
- [case-9b8bac5680e58daada3a](../../../../store/cases/case-9b8bac5680e58daada3a/07783b8487f55d819249fc632337f48a461889504642d293282c1e455ffb6591.json) · 结论：diagnosis, recommendation:3
  卡片版本：`07783b8487f55d819249fc632337f48a461889504642d293282c1e455ffb6591`
- [case-c6be08b1a56bd0fc8e88](../../../../store/cases/case-c6be08b1a56bd0fc8e88/39a7479ea5eae31dae4862da3a4a2941abccc1c2a3489a1f6a97dc99c19edcfa.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:4
  卡片版本：`39a7479ea5eae31dae4862da3a4a2941abccc1c2a3489a1f6a97dc99c19edcfa`
- [case-c9cc6663456a2ef02f89](../../../../store/cases/case-c9cc6663456a2ef02f89/ae6747eccb36d26241318b2258e46b0c5b7289bd01e525c168b0fbc5b8ab4ace.json) · 结论：diagnosis, recommendation:1
  卡片版本：`ae6747eccb36d26241318b2258e46b0c5b7289bd01e525c168b0fbc5b8ab4ace`
- [case-d53f19cb359b879b340c](../../../../store/cases/case-d53f19cb359b879b340c/fdb06a9c57661465138e471a87aa9c64a2610ed9246cc863781e5acd92e42761.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`fdb06a9c57661465138e471a87aa9c64a2610ed9246cc863781e5acd92e42761`
- [case-f749e3c70af1100c90d9](../../../../store/cases/case-f749e3c70af1100c90d9/c92c4d7503e18d5c1cc56cd928d3807e84d363082fcb2d1286d1f450b0bbb6c4.json) · 结论：recommendation:3, recommendation:4
  卡片版本：`c92c4d7503e18d5c1cc56cd928d3807e84d363082fcb2d1286d1f450b0bbb6c4`

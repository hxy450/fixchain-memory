# Stack 子项位置由父 alignContent 决定、子项 .align() 只对齐自身内容：混合对齐用 layoutGravity 或 position

ID：`lesson-92aee54a305ea0bde363` · 版本：9

[本主题](index.md)

## 何时使用

界面转换与巡检修复阶段，把 FrameLayout/CoordinatorLayout 的 layout_gravity、RelativeLayout 的 alignParent*/centerInParent、Compose Box 的 Modifier.align 或自定义 Layout 的 placeRelative 翻译为 ArkUI Stack 子项定位并确定叠层次序时；修复或编译清理删除 height('100%')、.align() 等定位手段时

## 适用情境

目标用 Stack 同时容纳对齐需求不同的子项：贴右下的角标（layout_gravity=end|bottom）、贴底的购买栏（Modifier.align(BottomCenter)）、FAB、多选浮层、按 placeRelative(x, (maxHeight - height) / 2) 纵向居中的文字；Stack 设了统一的 alignContent（常为 TopStart 或默认 Center）。映射参考或兄弟页可能把 layout_gravity 写成 .align(Alignment.X)。

## 例外与边界

- Stack 中只有一个需要定位的子项，或全部子项同向贴边时，直接改父 Stack 的 alignContent 即可

## 原因

Stack 按 alignContent 放置未撑满的子项；子项的 .align() 只设置自身内容在绘制区内的对齐（common.d.ts 对 align 的说明），内容尺寸的 Text 在 TopStart 的 Stack 里仍落在左上角；ArkUI Alignment 也没有 Compose 的 CenterStart。源端叠层通常后声明者绘制在上；子项带 elevation 或 translationZ 时，ViewGroup 先按 Z 排序再按声明顺序绘制（android-36.1 ViewGroup.buildOrderedChildList），只按声明顺序排会排错层。

## 做法

1. 每个 Stack 子项先区分“内容对齐”还是“在父容器中的位置”。同一 Stack 内各子项对齐不同时，目标 compatibleSdkVersion ≥ 20 可直接给子项写 .layoutGravity(LocalizedAlignment.BOTTOM_END 等)（common.d.ts，API 20 起）；低于 20 时用 .position({ left/right/top/bottom })、markAnchor，或满幅透明容器配 justifyContent/alignItems，并保留源 margin。
2. 已知容器宽高 W×H 时，layout_gravity=end|bottom 的角标也可写 position({ x: W - 子宽, y: H - 子高 })，或给该子项单独套一个 alignContent 为对应方向的 Stack。
3. 逐个核对源 Box 子项的 Modifier.align 与 placeRelative 公式：按公式纵向居中的文字，包一个满高 Column（justifyContent(FlexAlign.Center)、alignItems(HorizontalAlign.Start)，宽取源端比例），或给 Text 一个满高的框；规格或报告里的“底部对齐”要落到代码属性上。
4. 删除 height('100%')、.align() 等手段前，确认替代约束仍实现原来的位置；枚举名以 ArkUI SDK 为准，不照搬 Compose 的 Alignment 名称。
5. 叠层次序按源布局声明顺序复核（后声明者在上）；源端子项带 elevation/translationZ（框架 Widget.Material.Button 经 stateListAnimator 设置，见 android-36.1 res/anim/button_state_list_anim_material.xml），或运行时调用 bringToFront/addView 改变子项次序时，按改变后的实际绘制顺序排列，无法按序排列时补 zIndex。
6. Stack 里应贴顶的块不依赖默认对齐：写 alignContent(Alignment.Top) 或 position。

## 可选检查

- 沿用了映射参考或先例中的定位写法时，检索 .align(Alignment.，逐个确认它要的是内容对齐还是在父容器中的位置。

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
- [case-c6be08b1a56bd0fc8e88](../../../../store/cases/case-c6be08b1a56bd0fc8e88/39a7479ea5eae31dae4862da3a4a2941abccc1c2a3489a1f6a97dc99c19edcfa.json) · 结论：diagnosis, recommendation:2
  卡片版本：`39a7479ea5eae31dae4862da3a4a2941abccc1c2a3489a1f6a97dc99c19edcfa`
- [case-c9cc6663456a2ef02f89](../../../../store/cases/case-c9cc6663456a2ef02f89/ae6747eccb36d26241318b2258e46b0c5b7289bd01e525c168b0fbc5b8ab4ace.json) · 结论：diagnosis, recommendation:1
  卡片版本：`ae6747eccb36d26241318b2258e46b0c5b7289bd01e525c168b0fbc5b8ab4ace`
- [case-d53f19cb359b879b340c](../../../../store/cases/case-d53f19cb359b879b340c/fdb06a9c57661465138e471a87aa9c64a2610ed9246cc863781e5acd92e42761.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`fdb06a9c57661465138e471a87aa9c64a2610ed9246cc863781e5acd92e42761`
- [case-f749e3c70af1100c90d9](../../../../store/cases/case-f749e3c70af1100c90d9/c92c4d7503e18d5c1cc56cd928d3807e84d363082fcb2d1286d1f450b0bbb6c4.json) · 结论：recommendation:3, recommendation:4
  卡片版本：`c92c4d7503e18d5c1cc56cd928d3807e84d363082fcb2d1286d1f450b0bbb6c4`

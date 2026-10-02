# 贴合内容的描边、背景画在由内容定尺寸的节点自身，不用 width/height('100%') 覆盖层；源端描边不改尺寸时注意 .border() 计入测量

ID：`lesson-a58ebfe7a4c55b041b14` · 版本：3

[本主题](index.md)

## 何时使用

界面实现与规格映射阶段，翻译用 fillMaxSize()、matchContentSize 贴合内容的选中指示器、描边或背景，为高度由内容决定的行加铺满的背景层（滑删进度背景等），或把 Compose Modifier.border 这类只绘制、不改测量的修饰符落到 ArkUI 容器上时

## 适用情境

源端指示器或背景层以 fillMaxSize、matchContentSize 贴合某个由内容定尺寸的格子；目标准备在 Stack/Row 里叠一层 width/height('100%') 的节点来画描边或背景。也包括列表行里的 Stack 没有确定高度，准备放一层宽高 100% 的背景子节点；或源 border 画在调用方已定尺寸的盒内侧，目标容器自身不设宽高、尺寸由槽内容决定。

## 例外与边界

- 父节点有确定的宽高（显式数值，或已被外层约束定死）时，百分比层按该尺寸解析，可以使用

## 原因

ArkUI 的百分比尺寸在由内容定尺寸的父级里会向上取到最近的确定尺寸，把格子撑大（工程迁移陷阱表与设备实测一致）。来源中选中格内的 height('100%') 描边层解析到被撑高的 Tab 行高度，选中格变成约 299×597vp；与横向 Scroll 未定高叠加后，首帧只看得到前两项。列表行里的 100% 背景层同样会按更大的约束铺开，把行撑到整屏高。另一方面，在没有显式宽高的容器上写 .border()，来源 dump 显示描边计入了容器测量，盒子比内容大出描边宽度、后续卡片随之错位；Compose 的 Modifier.border 只在已定尺寸的盒内绘制，不改尺寸。

## 做法

1. 描边、背景直接写在内容节点上（.border()、.backgroundColor()、.borderRadius()），描边与内容的间距用 padding 表达；源端描边相对内容有内缩时，把内缩量拆到外层与内容节点的 padding 里。
2. 选中与未选中两态保留同样宽度的描边，未选中用 Color.Transparent，切换时尺寸不变。
3. 写完 grep width('100%') 与 height('100%')，逐处确认父级有确定尺寸。
4. 行或卡片的铺满背景改用 .background(builder) 画在容器自身，或用列表项自带的滑动操作（ListItem.swipeAction）。
5. 源端描边只绘制、不改尺寸时，先写明目标盒尺寸由谁决定：能拿到调用方尺寸就把宽高提升到带描边的节点上；尺寸只能由内容决定时，改用按 onSizeChange 回读的数值宽高叠一层 position({ x: 0, y: 0 }) + hitTestBehavior(HitTestMode.None) 的描边层（首帧会缺描边），规格验收写明“描边不改变盒尺寸”。

## 可选检查

- 源端描边不改尺寸而有疑问时，用 dumpLayout 核对带描边容器的 bounds 与内容子项一致。

来源支持：3 张卡 · 3 次迁移 · 2 个应用

## 来源（按需复核）

- [case-2018daf21990f553ec22](../../../../store/cases/case-2018daf21990f553ec22/28ef980edd82e29589d8923bf1fff263161ff6975ab9fe8a33e7149e781419c0.json) · 结论：diagnosis, recommendation:2
  卡片版本：`28ef980edd82e29589d8923bf1fff263161ff6975ab9fe8a33e7149e781419c0`
- [case-77c4d0c99ad4a6486b79](../../../../store/cases/case-77c4d0c99ad4a6486b79/0c0854b7bb53f48c15425a1148239e8e459db928eb8f9600f5e5b1e1cc5042f4.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`0c0854b7bb53f48c15425a1148239e8e459db928eb8f9600f5e5b1e1cc5042f4`
- [case-fc6df865cb042aec7af1](../../../../store/cases/case-fc6df865cb042aec7af1/725333df04b7bf7ef507cb28acc9e956d4e070ff49905447493a6f27eec530f2.json) · 结论：diagnosis, recommendation:2
  卡片版本：`725333df04b7bf7ef507cb28acc9e956d4e070ff49905447493a6f27eec530f2`

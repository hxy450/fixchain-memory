# 由内容定尺寸的父级（列表行、wrap_content 头部、FIT_CONTENT 半模态）里不写 width/height('100%')：描边背景画在节点自身，行内撑满用 Stretch；源端描边不改尺寸时注意 .border() 计入测量（定尺寸遮罩中的居中弹卡不在此列，宽度按源窗口规则）

ID：`lesson-a58ebfe7a4c55b041b14` · 版本：9

[本主题](index.md)

## 何时使用

界面实现与规格映射阶段，翻译用 fillMaxSize()、matchContentSize 贴合内容的选中指示器、描边或背景，为高度由内容决定的行加铺满的背景层（滑删进度背景等），或把 Compose Modifier.border 这类只绘制、不改测量的修饰符落到 ArkUI 容器上时；把 match_parent 高度翻译到 ListItem、列表行组件、折叠头部背景层或 bindSheet 内容根时；转换将被宿主嵌入的子组件（Fragment 转子组件）、确定根节点及各状态视图的高度约束时；为 GridView/ListView 条目补高度、好让子层撑满时

## 适用情境

源端指示器或背景层以 fillMaxSize、matchContentSize 贴合某个由内容定尺寸的格子；目标准备在 Stack/Row 里叠一层 width/height('100%') 的节点来画描边或背景。也包括列表行里的 Stack 没有确定高度，准备放一层宽高 100% 的背景子节点；或源 border 画在调用方已定尺寸的盒内侧，目标容器自身不设宽高、尺寸由槽内容决定。也包括源 match_parent 子视图位于 wrap_content 的行、AppBar 或 BottomSheet 容器中，实际随内容或兄弟高度；目标放进 List、ListItem、Scroll 或 FIT_CONTENT 半模态，准备直译为 height('100%')。也包括被宿主嵌入的子组件：源布局根节点与空态容器都是 wrap_content，在宿主 NestedScrollView 的 wrap_content 槽位里按内容取高；目标根 Column 与 loading/empty/error 各分支写 height('100%')，宿主把它放进 Scroll 内未设高度的 Column。 也包括 GridView/ListView 条目由内容定高，目标准备用 width('100%') 加 aspectRatio 或固定 vp 给条目定高，好让子层写 100%。 也包括 wrap_content 宽的 PopupWindow 内容是竖向 LinearLayout：一个定宽子项（如取色器）与若干 match_parent 的滑杆或自定义 View 并列，目标要为弹层与滑杆写出数值宽度。

## 例外与边界

- 父节点有确定的宽高（显式数值，或已被外层约束定死）时，百分比层按该尺寸解析，可以使用；为满足这一条而给行或格子补的高度取源端该项的实际测量结果，不用 aspectRatio、固定 vp 或 layoutWeight 凑
- 页面根 Stack 等定尺寸遮罩里的居中弹窗卡片：父级已定尺寸，宽度按源端窗口规则写（框架 AlertDialog 为屏宽 95% 减左右各 16dp），不适用本条，也不从本条取固定 vp 估值

## 原因

ArkUI 的百分比尺寸在由内容定尺寸的父级里会向上取到最近的确定尺寸，把格子撑大（工程迁移陷阱表与设备实测一致）。来源中选中格内的 height('100%') 描边层解析到被撑高的 Tab 行高度，选中格变成约 299×597vp；与横向 Scroll 未定高叠加后，首帧只看得到前两项。列表行里的 100% 背景层同样会按更大的约束铺开，把行撑到整屏高。另一方面，在没有显式宽高的容器上写 .border()，来源 dump 显示描边计入了容器测量，盒子比内容大出描边宽度、后续卡片随之错位；Compose 的 Modifier.border 只在已定尺寸的盒内绘制，不改尺寸。源 match_parent 直译成 height('100%') 时，单行或折叠头部会撑满整个 List 视口，半模态内容根会把 FIT_CONTENT 弹层撑到上限。被嵌子组件根节点的 '100%' 在 Scroll 的无界父链里会解析成视口高度，把首屏后续区块挤出。 为了让 100% 子层有确定父尺寸而用宽高比或经验值给行补高度，行高会与源端测量不符。

## 做法

1. 描边、背景直接写在内容节点上（.border()、.backgroundColor()、.borderRadius()），描边与内容的间距用 padding 表达；源端描边相对内容有内缩时，把内缩量拆到外层与内容节点的 padding 里。
2. 选中与未选中两态保留同样宽度的描边，未选中用 Color.Transparent，切换时尺寸不变。
3. 写完 grep width('100%') 与 height('100%')，逐处确认父级有确定尺寸。 需要给行或格子补高度时按源端该行的测量取值：源条目在 GridView/ListView 里时，行高＝条目内容按 UNSPECIFIED 测得的高（wrap_content 图片为密度放大后的固有高）加条目 padding，写在 GridItem/ListItem 上；去 Adapter.getView 的 setLayoutParams 与 padding、条目布局 XML 的 layout_height、内含图片的密度目录与像素尺寸里查。
4. 行或卡片的铺满背景改用 .background(builder) 画在容器自身，或用列表项自带的滑动操作（ListItem.swipeAction）。
5. 源端描边只绘制、不改尺寸时，先写明目标盒尺寸由谁决定：能拿到调用方尺寸就把宽高提升到带描边的节点上；尺寸只能由内容决定时，改用按 onSizeChange 回读的数值宽高叠一层 position({ x: 0, y: 0 }) + hitTestBehavior(HitTestMode.None) 的描边层（首帧会缺描边），规格验收写明“描边不改变盒尺寸”。
6. 行内交叉轴撑满（如行首竖条、拖拽柄随行高）用 alignSelf(ItemAlign.Stretch) 或明确尺寸；头部背景或遮罩层按源可见区域给显式高度（如工具栏高加头部块），或把背景画在容器自身。源 LinearLayout（含 wrap_content 的 PopupWindow 内容）在某轴为 wrap_content 时，该轴尺寸只由非 match_parent 子项决定（竖向 LinearLayout 取这些子项的最大宽加各自 margin，再加父 padding），match_parent 子项随后按该尺寸以 EXACTLY 重测；需要算出数值（弹层宽、自绘子项的测量宽）时按这个顺序，不让 match_parent 子项的偏好尺寸参与父级定宽，自定义 View 的偏好长度只在 AT_MOST/UNSPECIFIED 下生效。
7. 半模态内容根的 Scroll/Column 不写 height('100%')，由弹层上限约束后滚动；不写 100% 只解决高度，Scroll 还要设非 None 的 edgeEffect 才能在 FIT_CONTENT 弹层里拖动（见 lesson-df1f691759f84ba9e688 做法 3）。
8. 被嵌子组件按源布局根节点与各状态容器的 layout_height 映射：wrap_content 不写 height('100%')，空态居中用内容高度或 constraintSize 最小高度；宿主向无高度槽位嵌入组件前，读被嵌组件 build() 根与各状态分支的高度修饰，有百分比高度就先改组件或在槽位按源端尺寸给显式高度，再核对首屏后续区块仍可见。

## 可选检查

- 源端描边不改尺寸而有疑问时，用 dumpLayout 核对带描边容器的 bounds 与内容子项一致。
- 行或头部出现整屏高、或弹层被撑到上限时，检索该子树中的 '100%' 高度并确认其父级是否定高

来源支持：13 张卡 · 已知 8 次迁移（部分未记录） · 已知 7 个应用（部分未记录）

## 来源（按需复核）

- [case-17a1b7a8f9035398523a](../../../../store/cases/case-17a1b7a8f9035398523a/38ce90e0b87cb087dc752ad6a5c0231c518e191ade8839d2e06e1fe31af45d7f.json) · 结论：diagnosis, recommendation:1, recommendation:4, recommendation:5
  卡片版本：`38ce90e0b87cb087dc752ad6a5c0231c518e191ade8839d2e06e1fe31af45d7f`
- [case-1ff61bb8eea97c7cac7f](../../../../store/cases/case-1ff61bb8eea97c7cac7f/cc69235df441f52f2023b37f688670cb3c8ffddec1751b9653b3aefd35c321f7.json) · 结论：recommendation:2
  卡片版本：`cc69235df441f52f2023b37f688670cb3c8ffddec1751b9653b3aefd35c321f7`
- [case-2018daf21990f553ec22](../../../../store/cases/case-2018daf21990f553ec22/28ef980edd82e29589d8923bf1fff263161ff6975ab9fe8a33e7149e781419c0.json) · 结论：diagnosis, recommendation:2
  卡片版本：`28ef980edd82e29589d8923bf1fff263161ff6975ab9fe8a33e7149e781419c0`
- [case-47b9e1107e4e4ecd40bd](../../../../store/cases/case-47b9e1107e4e4ecd40bd/87b0c345ca3fa21bf70b01c74e3a2714a0880c4a2e5531942fe4d81a24d85b98.json) · 结论：recommendation:1
  卡片版本：`87b0c345ca3fa21bf70b01c74e3a2714a0880c4a2e5531942fe4d81a24d85b98`
- [case-4f627840679361f165a3](../../../../store/cases/case-4f627840679361f165a3/8b0f7cc40d821777a77dc3bf68c6739f335039023414e9bcb04404d5b4ac02e8.json) · 结论：recommendation:1
  卡片版本：`8b0f7cc40d821777a77dc3bf68c6739f335039023414e9bcb04404d5b4ac02e8`
- [case-50d5978491b9ba48b899](../../../../store/cases/case-50d5978491b9ba48b899/1d0dc9fa70cf068c678afcbb27308a85366c39290f03c618b36fc6bcf443b897.json) · 结论：diagnosis, recommendation:4
  卡片版本：`1d0dc9fa70cf068c678afcbb27308a85366c39290f03c618b36fc6bcf443b897`
- [case-5916095777c21ec74389](../../../../store/cases/case-5916095777c21ec74389/70e9253633bc4dd9bf5141a3152c9235dc38fad10033b18499d7c30acdf14804.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`70e9253633bc4dd9bf5141a3152c9235dc38fad10033b18499d7c30acdf14804`
- [case-77c4d0c99ad4a6486b79](../../../../store/cases/case-77c4d0c99ad4a6486b79/0c0854b7bb53f48c15425a1148239e8e459db928eb8f9600f5e5b1e1cc5042f4.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`0c0854b7bb53f48c15425a1148239e8e459db928eb8f9600f5e5b1e1cc5042f4`
- [case-821ade66a5ad47cdea22](../../../../store/cases/case-821ade66a5ad47cdea22/d6a6fd477dc2843095f41c2605944d99e05dcc8babde979368d788f5c16dad20.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`d6a6fd477dc2843095f41c2605944d99e05dcc8babde979368d788f5c16dad20`
- [case-9058ac868b6feb3a04e0](../../../../store/cases/case-9058ac868b6feb3a04e0/d8e013afe2706da7f1b19c1a0d603c05f971b4ebc0c4542f6fb5e8a956b3ebc4.json) · 结论：recommendation:2
  卡片版本：`d8e013afe2706da7f1b19c1a0d603c05f971b4ebc0c4542f6fb5e8a956b3ebc4`
- [case-cdc263993782c99990b7](../../../../store/cases/case-cdc263993782c99990b7/65fe34b35c12ba1fb3fa8932c505408e3d127754cf0883d637a7da9585330199.json) · 结论：recommendation:2
  卡片版本：`65fe34b35c12ba1fb3fa8932c505408e3d127754cf0883d637a7da9585330199`
- [case-dadda7b6820516f5f415](../../../../store/cases/case-dadda7b6820516f5f415/550a74cac527a7a37d9d1cb7aae1e487f44b8b49eb75ea53d1918d9a05d3ca0b.json) · 结论：recommendation:6
  卡片版本：`550a74cac527a7a37d9d1cb7aae1e487f44b8b49eb75ea53d1918d9a05d3ca0b`
- [case-fc6df865cb042aec7af1](../../../../store/cases/case-fc6df865cb042aec7af1/725333df04b7bf7ef507cb28acc9e956d4e070ff49905447493a6f27eec530f2.json) · 结论：diagnosis, recommendation:2
  卡片版本：`725333df04b7bf7ef507cb28acc9e956d4e070ff49905447493a6f27eec530f2`

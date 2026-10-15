# 由内容定尺寸的父级（列表行、wrap_content 头部、FIT_CONTENT 半模态）里不写 100% 尺寸：背景画在节点自身，撑满用 Stretch

ID：`lesson-a58ebfe7a4c55b041b14` · 版本：10

[本主题](index.md)

## 何时使用

界面实现与规格映射阶段，翻译用 fillMaxSize()、matchContentSize 贴合内容的选中指示器、描边或背景，为高度由内容决定的行加铺满的背景层（滑删进度背景等），或把 match_parent 高度翻译到 ListItem、列表行组件、折叠头部背景层或 bindSheet 内容根时

## 适用情境

源端指示器或背景层以 fillMaxSize、matchContentSize 贴合由内容定尺寸的格子；源 match_parent 子视图位于 wrap_content 的行、AppBar 或 BottomSheet 容器中，实际随内容或兄弟高度。目标准备在 Stack/Row、List、ListItem、Scroll 或 FIT_CONTENT 半模态里叠一层或直译为 width/height('100%') 的节点；或为了让条目里的铺满层有确定父尺寸，准备用 aspectRatio、固定 vp 给由内容定高的网格项或列表项定高。

## 例外与边界

- 父节点有确定的宽高（显式数值，或已被外层约束定死）时，百分比层按该尺寸解析，可以使用
- 页面根 Stack 等定尺寸遮罩里的居中弹窗卡片：父级已定尺寸，宽度按源端窗口规则写。框架 Material AlertDialog 的最小宽取主题 windowMinWidthMinor/Major（SDK platforms/android-<api>/data/res/values/dimens.xml 的 dialog_min_width_minor 竖屏 95%、dialog_min_width_major 横屏 65%，android-36 中如此），背景 drawable/dialog_background_material.xml 另有 16dp inset；不适用本条，也不从本条取固定 vp 估值
- 占剩余高度的内容区或被宿主嵌入的满高组件，按宿主有界槽位的规则处理

## 原因

ArkUI 的百分比尺寸在由内容定尺寸的父级里会向上取到最近的确定尺寸，把格子、行或头部撑大：选中格被撑到行高，列表行与折叠头部撑满整个 List 视口，半模态内容根把 FIT_CONTENT 弹层撑到上限。

## 做法

1. 描边、背景直接写在内容节点上（.border()、.backgroundColor()、.borderRadius()），描边与内容的间距用 padding 表达；源端描边相对内容有内缩时，把内缩量拆到外层与内容节点的 padding 里。
2. 选中与未选中两态保留同样宽度的描边，未选中用 Color.Transparent，切换时尺寸不变。
3. 行或卡片的铺满背景改用 .background(builder) 画在容器自身，或用列表项自带的滑动操作（ListItem.swipeAction）。
4. 行内交叉轴撑满（如行首竖条、拖拽柄随行高）用 alignSelf(ItemAlign.Stretch) 或明确尺寸；行本身未定高时，Stretch 子项会取到更外层的确定尺寸并把行与卡片撑开，先给行定高再让子项撑满（按钮行竖分隔线见 lesson-2a07020daf9a7d8a60a3）；头部背景或遮罩层按源可见区域给显式高度（如工具栏高加头部块），或把背景画在容器自身。补的高度取源端该行的实际测量结果，不按宽高比或经验值臆造：源条目在 GridView/ListView 里时，行高＝条目内容按 UNSPECIFIED 测得的高（wrap_content 图片为密度放大后的固有高）＋条目 padding，写在 GridItem/ListItem 上。
5. 半模态内容根的 Scroll/Column 不写 height('100%')，由弹层上限约束后滚动。
6. 写完检索 width('100%') 与 height('100%')，逐处确认父级有确定尺寸。

## 可选检查

- 行或头部出现整屏高、或弹层被撑到上限时，检索该子树中的 '100%' 高度并确认其父级是否定高。

来源支持：9 张卡 · 6 次迁移 · 6 个应用

## 来源（按需复核）

- [case-1ff61bb8eea97c7cac7f](../../../../store/cases/case-1ff61bb8eea97c7cac7f/cc69235df441f52f2023b37f688670cb3c8ffddec1751b9653b3aefd35c321f7.json) · 结论：recommendation:2
  卡片版本：`cc69235df441f52f2023b37f688670cb3c8ffddec1751b9653b3aefd35c321f7`
- [case-2018daf21990f553ec22](../../../../store/cases/case-2018daf21990f553ec22/28ef980edd82e29589d8923bf1fff263161ff6975ab9fe8a33e7149e781419c0.json) · 结论：diagnosis, recommendation:2
  卡片版本：`28ef980edd82e29589d8923bf1fff263161ff6975ab9fe8a33e7149e781419c0`
- [case-47b9e1107e4e4ecd40bd](../../../../store/cases/case-47b9e1107e4e4ecd40bd/87b0c345ca3fa21bf70b01c74e3a2714a0880c4a2e5531942fe4d81a24d85b98.json) · 结论：recommendation:1
  卡片版本：`87b0c345ca3fa21bf70b01c74e3a2714a0880c4a2e5531942fe4d81a24d85b98`
- [case-4f627840679361f165a3](../../../../store/cases/case-4f627840679361f165a3/8b0f7cc40d821777a77dc3bf68c6739f335039023414e9bcb04404d5b4ac02e8.json) · 结论：recommendation:1
  卡片版本：`8b0f7cc40d821777a77dc3bf68c6739f335039023414e9bcb04404d5b4ac02e8`
- [case-50d5978491b9ba48b899](../../../../store/cases/case-50d5978491b9ba48b899/1d0dc9fa70cf068c678afcbb27308a85366c39290f03c618b36fc6bcf443b897.json) · 结论：recommendation:4
  卡片版本：`1d0dc9fa70cf068c678afcbb27308a85366c39290f03c618b36fc6bcf443b897`
- [case-9058ac868b6feb3a04e0](../../../../store/cases/case-9058ac868b6feb3a04e0/d8e013afe2706da7f1b19c1a0d603c05f971b4ebc0c4542f6fb5e8a956b3ebc4.json) · 结论：recommendation:2
  卡片版本：`d8e013afe2706da7f1b19c1a0d603c05f971b4ebc0c4542f6fb5e8a956b3ebc4`
- [case-bf55dc1aedfb0f2a965e](../../../../store/cases/case-bf55dc1aedfb0f2a965e/bcb7663fe953c49cc6b18f293ae448fe649838e3a6f0e8e0e2d31020c4836d2d.json) · 结论：diagnosis, recommendation:2
  卡片版本：`bcb7663fe953c49cc6b18f293ae448fe649838e3a6f0e8e0e2d31020c4836d2d`
- [case-dadda7b6820516f5f415](../../../../store/cases/case-dadda7b6820516f5f415/550a74cac527a7a37d9d1cb7aae1e487f44b8b49eb75ea53d1918d9a05d3ca0b.json) · 结论：recommendation:6
  卡片版本：`550a74cac527a7a37d9d1cb7aae1e487f44b8b49eb75ea53d1918d9a05d3ca0b`
- [case-fc6df865cb042aec7af1](../../../../store/cases/case-fc6df865cb042aec7af1/725333df04b7bf7ef507cb28acc9e956d4e070ff49905447493a6f27eec530f2.json) · 结论：diagnosis, recommendation:2
  卡片版本：`725333df04b7bf7ef507cb28acc9e956d4e070ff49905447493a6f27eec530f2`

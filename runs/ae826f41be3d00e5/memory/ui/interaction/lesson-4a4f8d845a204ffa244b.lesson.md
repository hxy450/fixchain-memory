# Stack 上层全尺寸容器和页面级遮罩会参与命中测试：不处理点击的覆盖层显式 Transparent，贴底内容栏直接锚定而不套全屏壳，条件遮罩用根 Stack 条件子节点

ID：`lesson-4a4f8d845a204ffa244b` · 版本：2

[本主题](index.md)

## 何时使用

界面实现与巡检修复阶段，把 FrameLayout 或 Compose Box 叠放层转成 ArkUI Stack、确定各层 hitTestBehavior 与贴底栏的定位方式时；为页面加保存中、引导等全屏遮罩时

## 适用情境

源 FrameLayout 中较晚声明、z 序更高的 match_parent 容器本身不可点击却覆盖下方按钮（Android 非 clickable 视图不消费触摸）；目标对应子层是 width/height('100%') 的容器；或页面要在带安全区 padding 的根容器上加全屏遮罩。也包括源 Compose Box 中返回按钮等可点击覆盖层之后，还有以 Modifier.align(Alignment.BottomCenter) 贴底、按内容定高的底栏，目标 Stack 的 alignContent 改为 TopStart 后需要另找贴底方式。

## 原因

ArkUI 中没有 onClick 的容器同样参与命中测试（HitTestMode.Default 会阻塞兄弟），全尺寸上层会吞掉下层点击，hilog 表现为 Touch test result is empty。为还原源端 z 序重排子节点后，原先“浮层设 Transparent”的标注会落在错误的层上；调整对齐或几何会放大覆盖区。.overlay() 挂条件 builder 在条件为假时仍会产生拦截触摸的层，挂在带 padding 的容器上又只覆盖内容盒、盖不到底部安全区。另一应用中巡检修复者为让底栏贴底，在返回按钮之后新增 width/height('100%') 的 Column{ Blank(); 底栏 } 作定位壳；这个后声明、默认命中模式的全屏壳盖住了左上角返回按钮，点击无响应，直到给按钮加 zIndex 才恢复。

## 做法

1. 按最终声明顺序逐层检查：位于可点击兄弟之上、覆盖其区域且自身不处理点击的容器，显式写 hitTestBehavior(HitTestMode.Transparent)；重排子节点或修改对齐与几何后重新核对。
2. 源端按内容定高、align(BottomCenter) 贴底的底栏，在 Stack 中保持自身尺寸并直接锚到底部（position 的 bottom 边或 RelativeContainer 的对齐规则），不用满屏 Column + Blank 作定位壳；确需全屏壳时给壳设 Transparent，或让可点击的覆盖控件最后声明、提高 zIndex。
3. 页面级全屏遮罩用无 padding 的根 Stack 条件子节点实现（条件为假时不产生节点），不在带 padding 的容器上用 .overlay() 挂条件 builder；复用同仓遮罩时连同挂载层级一起复用。

## 可选检查

- 调整 Stack 对齐、上层几何或新增定位壳后，对被覆盖区域的按钮逐个实际点击（不只看节点 clickable 与 bounds），检查 hilog 有无 Touch test result is empty。

## 来源（按需复核）

- case-37ef7d33ab4655385e6f · 结论：recommendation:3, recommendation:4
  卡片版本：`88751aad836b72f3c464d8020b00b1f0292a8c683547ef71fdc19979ac8ed972`
- case-57a208ad2e9541272704 · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`aeed6c0400b8e3633a7519cb161b7f7c5a7705890598067729231649087916b4`
- case-7d423b2bf98cdaabda82 · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`6f73cfbf4411b268f35a5835fb6a075e76a92a73aa629564da18c78946a43ecb`

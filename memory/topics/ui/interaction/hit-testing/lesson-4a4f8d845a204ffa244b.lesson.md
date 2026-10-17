# Stack 上层全尺寸容器和页面级遮罩会参与命中测试：不处理点击的覆盖层显式 Transparent，贴底内容栏直接锚定而不套全屏壳，条件遮罩与一次性动效层用根 Stack 条件子节点

ID：`lesson-4a4f8d845a204ffa244b` · 版本：8 · 阶段：execute/repair · 主题：[ui/interaction/hit-testing](index.md)

概要：不处理点击的全尺寸覆盖层显式设 Transparent 命中

信号：`hitTestBehavior`, `HitTestMode.Transparent`, `HitTestMode.None`, `FrameLayout`, `Modifier.align`, `alignContent`, `zIndex`, `Touch test result is empty`

## 何时使用

界面实现与巡检修复阶段，把 FrameLayout 或 Compose Box 叠放层转成 ArkUI Stack、确定各层 hitTestBehavior 与贴底栏的定位方式时；为页面加保存中、引导等全屏遮罩时；实现彩纸等一次性全屏动效的覆盖层时

## 适用情境

源 FrameLayout 中较晚声明、z 序更高的 match_parent 容器本身不可点击却覆盖下方按钮（Android 非 clickable 视图不消费触摸）；目标对应子层是 width/height('100%') 的容器；或页面要在带安全区 padding 的根容器上加全屏遮罩。也包括源 Compose Box 中返回按钮等可点击覆盖层之后，还有以 Modifier.align(Alignment.BottomCenter) 贴底、按内容定高的底栏，目标 Stack 的 alignContent 改为 TopStart 后需要另找贴底方式。也包括源端在触发瞬间向窗口根视图添加全屏、不可点击的动效层并在播完后移除，目标改成常驻挂载、带 zIndex 的全屏自定义组件，只给内部 Canvas 设 HitTestMode.None。也包括按钮之上叠有同尺寸、不可点击的自绘进度环或加载圈（源端触摸落到下层按钮），目标 Stack 保留 z 序而点击只挂在最底层图片上。

## 原因

ArkUI 中没有 onClick 的容器同样参与命中测试（HitTestMode.Default 会阻塞兄弟），全尺寸上层会吞掉下层点击，hilog 表现为 Touch test result is empty。为还原源端 z 序重排子节点后，原先“浮层设 Transparent”的标注会落在错误的层上；调整对齐或几何会放大覆盖区。.overlay() 挂条件 builder 在条件为假时仍会产生拦截触摸的层，挂在带 padding 的容器上又只覆盖内容盒、盖不到底部安全区。另一应用中巡检修复者为让底栏贴底，在返回按钮之后新增 width/height('100%') 的 Column{ Blank(); 底栏 } 作定位壳；这个后声明、默认命中模式的全屏壳盖住了左上角返回按钮，点击无响应，直到给按钮加 zIndex 才恢复。另一应用把完成彩纸组件无条件挂在日视图、月历弹层和详情弹层上（100% 宽高、zIndex 100），空闲时只清空画布；内部 Canvas 设了 None，外层组件节点仍拦截，日视图不能点击和滑动，改为仅在播放期间条件挂载才恢复。

## 做法

1. 按最终声明顺序逐层检查：位于可点击兄弟之上、覆盖其区域且自身不处理点击的容器，显式写 hitTestBehavior(HitTestMode.Transparent)；重排子节点或修改对齐与几何后重新核对。
2. 源端按内容定高、align(BottomCenter) 贴底的底栏，在 Stack 中保持自身尺寸并直接锚到底部（position 的 bottom 边或 RelativeContainer 的对齐规则），不用满屏 Column + Blank 作定位壳；确需全屏壳时给壳设 Transparent，或让可点击的覆盖控件最后声明、提高 zIndex。
3. 页面级全屏遮罩用无 padding 的根 Stack 条件子节点实现（条件为假时不产生节点），不在带 padding 的容器上用 .overlay() 挂条件 builder；复用同仓遮罩时连同挂载层级一起复用。
4. 一次性全屏动效（彩纸、提示动画）按源端生命周期只在播放期间条件渲染，结束或取消回调里移除；不要让全屏组件常驻，只靠内部子节点的 HitTestMode.None 放行。经 OverlayManager.addComponentContent 挂的窗口级层（如拖拽阴影）同样只在源端显示时段挂载、结束即 removeComponentContent；确需常驻时根用 Stack 等系统容器并随交互态切换命中模式，自定义组件作 ComponentContent 根时外层代理节点按缺省命中，内层 None 不起作用（Builder 根为自定义组件或 if/else 等语法节点时会额外生成不能设属性的 BuilderProxyNode，文档给出的绕法是用容器组件包裹并给容器设 HitTestMode.Transparent；HarmonyOS 文档 arkts-user-defined-arktsnode-buildernode，访问于 2026-10-17）。
5. 按钮上叠的进度环、加载层同样逐个决定命中：纯展示节点设 Transparent，或把 onClick 挂在整个 Stack 容器上，不只挂在最底层图片。

## 可选检查

- 调整 Stack 对齐、上层几何或新增定位壳后，对被覆盖区域的按钮逐个实际点击（不只看节点 clickable 与 bounds），检查 hilog 有无 Touch test result is empty。
- 一次性动效层改动后，空闲态用 dumpLayout 确认该节点不存在，再实测点击、横滑与折叠。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [SaveButton 授权回调只做快速写入，下载放点击前](../../../app/media/lesson-089bb378b1ec034a3e84.lesson.md)（共享 1 张卡）
- [Stack 子项 .align() 无效，对齐用满高容器](../../layout/constraints/lesson-92aee54a305ea0bde363.lesson.md)（共享 1 张卡）
- [锚点坐标在点击回调即时取，onAreaChange 只兜底](lesson-963bf871aa4e910a8fc8.lesson.md)（共享 1 张卡）
- [手势起点 Image 写 draggable(false)](../gestures/lesson-b30da57443f68ab9046a.lesson.md)（共享 1 张卡）
- [门面同步路径也要有源懒加载 getter 的回退来源](../../../app/playback/lesson-cd4a69e85ec59eabf5b9.lesson.md)（共享 1 张卡）

来源支持：7 张卡 · 已知 5 次迁移（部分未记录） · 已知 5 个应用（部分未记录）

## 来源（按需复核）

- [case-37ef7d33ab4655385e6f](../../../../../store/cases/case-37ef7d33ab4655385e6f/fdcf6c3cd31bc1665c4c5019cb403126011d55c2fef18000c729355e6c5af9ee.json) · 结论：rec-5a94b8f0f4, rec-42fbc9f395
  卡片版本：`fdcf6c3cd31bc1665c4c5019cb403126011d55c2fef18000c729355e6c5af9ee`
- [case-51d51ad98738e338df19](../../../../../store/cases/case-51d51ad98738e338df19/4b4648a54d0b19a84c842088554c0b057c5c8941db9a7d98ae885a39678a9db7.json) · 结论：diagnosis, rec-9a57720e21
  卡片版本：`4b4648a54d0b19a84c842088554c0b057c5c8941db9a7d98ae885a39678a9db7`
- [case-57a208ad2e9541272704](../../../../../store/cases/case-57a208ad2e9541272704/8d2a2903f578b837bbe4fbae23c3df7cbdd8897003895ed0d906609949fd4c6d.json) · 结论：diagnosis, rec-891c75d0b8, rec-5cf5d60ea9, rec-869edbf919
  卡片版本：`8d2a2903f578b837bbe4fbae23c3df7cbdd8897003895ed0d906609949fd4c6d`
- [case-7d423b2bf98cdaabda82](../../../../../store/cases/case-7d423b2bf98cdaabda82/8441ff125fb267f472ee908947f3d00c83fcf6594fca7b15991b175092fe51b9.json) · 结论：diagnosis, rec-6b81157d1d, rec-9834580632, rec-495d7fffc8
  卡片版本：`8441ff125fb267f472ee908947f3d00c83fcf6594fca7b15991b175092fe51b9`
- [case-8809177953953374a01e](../../../../../store/cases/case-8809177953953374a01e/0f0a55473275f4a825fd345992d4bfd1b18db95262ea8d48b11572f0c0dfc81f.json) · 结论：rec-0876f88d88, rec-4cab3efe0b
  卡片版本：`0f0a55473275f4a825fd345992d4bfd1b18db95262ea8d48b11572f0c0dfc81f`
- [case-9b8bac5680e58daada3a](../../../../../store/cases/case-9b8bac5680e58daada3a/07783b8487f55d819249fc632337f48a461889504642d293282c1e455ffb6591.json) · 结论：diagnosis, rec-cbb7752238, rec-6745106cf7
  卡片版本：`07783b8487f55d819249fc632337f48a461889504642d293282c1e455ffb6591`
- [case-d38fbc2e9b64b7c3338b](../../../../../store/cases/case-d38fbc2e9b64b7c3338b/0c81ee0d0f88b740ca143860bd386d61a44268d1703fbe3e4e239c5375013a71.json) · 结论：diagnosis, rec-ca63e5f2d4
  卡片版本：`0c81ee0d0f88b740ca143860bd386d61a44268d1703fbe3e4e239c5375013a71`

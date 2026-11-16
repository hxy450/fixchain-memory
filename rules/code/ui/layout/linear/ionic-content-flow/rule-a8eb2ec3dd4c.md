# Ionic 内容区没写 flex-grow 或 ion-padding 时，按内容流写，不加 layoutWeight

审的是：代码
触发（任一种）：
- 读到：IonContent 里依次是 IonChip、Swiper、IonButton，源上没有 flex-grow、height: 100% 或 ion-padding；写错的样子：目标给 Swiper、外层 Column 或 Image 加了 .layoutWeight(1)、slide Column .height('100%')，内容 Column 加了水平 .padding，按钮被压到屏底
适用范围：把 Ionic / Web 的模态内容区翻成 ArkUI Column / Stack / Swiper 布局时
做法：
- 先在源里查 flex-grow、height:100%、ion-padding；都没有就按块级内容流写：不给 Swiper、外层 Column、图片加 layoutWeight，不加容器水平 padding
- 只保留源上逐个元素的 margin（如 marginLeft），按钮紧跟在轮播后面
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 去掉 layoutWeight 链、去掉容器水平 padding：修复后插图满宽，分页点和按钮紧跟轮播（出处：卡里修好并验证过）
未核实：卡里的目标 SDK 是 26.0.0，本机核实用的是 API 23
来源：1 张卡，1 个应用
- case-acd91ce1ab3d2798a4fa（Countdate）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 1 ← 诊断

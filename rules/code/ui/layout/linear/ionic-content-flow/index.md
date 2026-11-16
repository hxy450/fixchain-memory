# Ionic 内容区的纵向排布（IonContent）

agent 会看到什么：读到 IonContent 里依次排着 IonChip、Swiper、IonButton 等，源上没有 flex-grow、height: 100% 或 ion-padding；产物里外层 Column、Swiper、Image 上的 .layoutWeight(1)、height('100%') 和内容 Column 的水平 .padding

## 规矩

- rule-a8eb2ec3dd4c｜Ionic 内容区没写 flex-grow 或 ion-padding 时，按内容流写，不加 layoutWeight｜读到：IonContent 里依次是 IonChip、Swiper、IonButton，源上没有 flex-grow、height: 100% 或 ion-padding；写错：目标给 Swiper、外层 Column 或 Image 加了 .layoutWeight(1)、slide Column .height('100%')，内容 Column 加了水平 .padding，按钮被压到屏底

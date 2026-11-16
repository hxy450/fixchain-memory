# Ionic 组件的默认样式和子项顺序

agent 会看到什么：读到 setupIonicReact({ mode })、IonCard / IonCardHeader 这类 Ionic 组件只写了部分 inline style，或容器是 flex-direction: *-reverse；产物里只照 inline style 写的 Text 和卡片外观、按 DOM 序排的子组件

## 规矩

- rule-3e884dc0889c｜翻译 Ionic 组件时三层样式合并后再写 ArkUI，-reverse 容器按渲染序排子组件｜读到：源端 setupIonicReact({ mode: 'ios' })，IonCardHeader 里 DOM 序是 IonCardSubtitle → IonCardTitle，inline style 只写了 fontSize；写错：目标按 DOM 序先写副标题 Text 再写标题 Text；副标题没有 .textCase(TextCase.UpperCase)、.fontWeight(...)、.letterSpacing(...)；卡片只有 .borderRadius(...)，没有 .shadow(...)

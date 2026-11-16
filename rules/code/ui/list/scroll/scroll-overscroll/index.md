# ScrollView 的越界模式

agent 会看到什么：读到 <ScrollView> 写了或没写 android:overScrollMode；产物里 Scroll 的 .edgeEffect(...)

## 规矩

- rule-4197074ae2ec｜ScrollView 转 Scroll 时按源端越界模式写 edgeEffect，未声明也要写｜读到：<ScrollView> 没写 android:overScrollMode（默认 ifContentScrolls），或写了 always / never；写错：Scroll 没有 .edgeEffect(...)；或写了 .edgeEffect(EdgeEffect.Spring) 却没带 { alwaysEnabled: false }，内容不满一屏也回弹

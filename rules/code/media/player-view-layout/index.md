# 播放器视图的尺寸和层级

agent 会看到什么：读到布局里 match_parent 的 PlayerView（没写 app:resize_mode），或播放时 addView(播放器 View, 0) 挂到 item 根布局的最底层；产物里 XComponent / Video 直接写 100% 宽高被拉伸，或放进封面区、没铺满 item

## 规矩

- rule-1d6ce312b535｜PlayerView match_parent 转 XComponent 时按视频宽高比内接算尺寸｜读到：布局里 PlayerView 的 layout_width / layout_height 为 match_parent，没写 app:resize_mode；写错：XComponent(SURFACE) 直接 .width('100%').height('100%')，横屏或宽高比不同时画面被拉伸
- rule-e73dba3db74f｜播放器运行时 addView 到 item 根部时，Video 放在根 Stack 最底层铺满，不放进封面区｜读到：Fragment 或 Adapter 播放时用 addView(播放器 View, 0) 把它挂到 item 根 ConstraintLayout 的最底层，不带 XML 约束；XML 里的自定义封面/控制视图只夹在顶栏和按钮行之间；写错：Video 放在顶栏和按钮行之间的 layoutWeight(1) 区里（和封面同一个 Stack），没有铺满 item；视频从标题行下方才开始

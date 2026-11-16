# Fragment 换页的自定义动画

agent 会看到什么：读到 FragmentTransaction.setCustomAnimations(…) 配 res/anim 资源，或先用动画辅助方法缩放列表项再 replace fragment；产物里只有 pushPathByName(...)，对应 NavDestination 上没有 .customTransition(...)

## 规矩

- rule-1d513f4f2b46｜Fragment 换页带自定义动画时，目标 NavDestination 写 customTransition｜读到：源码进入详情或覆盖页面时用 FragmentTransaction.setCustomAnimations(…) 配 res/anim 资源，或先用动画辅助方法缩放列表项再 replace fragment；写错：目标只写 navPathStack.pushPathByName(...)，对应 NavDestination 上没有 .customTransition(...)，走 Navigation 默认滑入；缩放层也没有

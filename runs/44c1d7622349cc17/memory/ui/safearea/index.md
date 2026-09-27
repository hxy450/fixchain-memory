# ui/safearea

沉浸式安全区：避让区测量（状态栏、导航指示条），全屏页底部按钮与贴底弹层的避让

[上一级](../index.md)

## 本级经验

- [全屏窗口的底部避让：导航指示条取 bottomRect，贴底按钮与 bindSheet 内容都要叠加避让值](lesson-0e1c846868f2683cc280.lesson.md)
  - 时机：沉浸式安全区实现阶段，测量导航指示条避让区，并为底部按钮行或贴底弹层确定底部间距时
  - 情境：目标页面在 setWindowLayoutFullScreen(true) 下用 getWindowAvoidArea 测避让值，写入页面或全局窗口模型；Android 源布局的底部按钮行、底部 sheet 没有导航栏间距（源窗口不延伸到导航栏下，BottomSheetDialog 由系统处理 inset）。

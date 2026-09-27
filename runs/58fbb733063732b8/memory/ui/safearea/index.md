# ui/safearea

沉浸式安全区：避让区测量与 px/vp 换算（状态栏、导航指示条），系统栏图标深浅，全屏页底部按钮与贴底弹层的避让，逐页落实前景避让

[上一级](../index.md)

## 本级经验

- [getWindowAvoidArea 与 windowRect 的数值是 px：写入供 padding 消费的窗口模型前先 px2vp](lesson-cf111aadb8804649b578.lesson.md)
  - 时机：沉浸式安全区实现阶段，在 EntryAbility 或窗口服务里把避让区、窗口尺寸写进共享窗口模型时
  - 情境：目标用 setWindowLayoutFullScreen(true) 全屏，EntryAbility 通过 getWindowAvoidArea 取状态栏、导航条高度，通过 getWindowProperties().windowRect 取窗口尺寸，写入 AppStorageV2 共享的窗口模型；各页把这些值直接放进 .padding()/.height()，按 vp 解释。
- [全屏窗口的底部避让：导航指示条取 bottomRect，贴底按钮与 bindSheet 内容都要叠加避让值](lesson-0e1c846868f2683cc280.lesson.md)
  - 时机：沉浸式安全区实现阶段，测量导航指示条避让区，并为底部按钮行或贴底弹层确定底部间距时
  - 情境：目标页面在 setWindowLayoutFullScreen(true) 下用 getWindowAvoidArea 测避让值，写入页面或全局窗口模型；Android 源布局的底部按钮行、底部 sheet 没有导航栏间距（源窗口不延伸到导航栏下，BottomSheetDialog 由系统处理 inset）。
- [系统栏图标深浅按源端状态栏配置设置，不照搬沉浸式模板的浅色文字默认值](lesson-824031d5fddf81036b54.lesson.md)
  - 时机：沉浸式窗口配置阶段，调用 setWindowSystemBarProperties 设置 statusBarContentColor/navigationBarContentColor 时
  - 情境：目标全屏窗口把系统栏背景设为透明，页面内容延伸到状态栏下；Android 源端 BaseActivity/主题用 ImmersionBar darkMode(true)、windowLightStatusBar 或白色状态栏配深色图标；沉浸式 skill 示意写“透明背景 + 浅色文字”。

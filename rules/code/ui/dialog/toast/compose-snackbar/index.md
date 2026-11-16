# Compose 的 Snackbar 和 SnackbarHost

agent 会看到什么：读到源端 SnackbarHostState.showSnackbar(message, actionLabel = …) 没写 duration、Scaffold 里只有一个 SnackbarHost，或自定义组件委托 material3 Snackbar；交回的提示条一律 setTimeout 4000、多个底部浮层并存，或几何是凭记忆写死的常量

## 通用查法

### 源端 material3 Snackbar 没写的参数，按依赖版本到库源码查默认值，写成显式的时长和几何

审的是：代码
触发（任一种）：
- 读到：源端调 SnackbarHostState.showSnackbar(…) 没写 duration，或自定义组件委托 androidx.compose.material3.Snackbar、只覆盖部分参数；写错的样子：目标自写的提示条一律 setTimeout(…, 4000)，或写死凭记忆的 minHeight、内距常量
适用范围：Compose Material3 的 Snackbar 迁成 ArkUI 自写提示条时
做法：
- 在源工程的 Gradle 依赖里查 androidx.compose.material3:material3 的版本（用 compose BOM 的按 BOM 映射）
- 到这个版本的库源码读没写的参数的默认值：showSnackbar 的 duration 按有无 actionLabel 取（无 action 为 Short，有 action 为 Indefinite），几何读 SnackbarTokens 和 Snackbar.kt
- 写成目标端显式的毫秒时长和 vp 几何；取不到的在报告里标为缺口，不写成带库出处注释的猜测值
针对本应用要查的：
- 应用依赖的 material3 版本：源工程 Gradle 构建脚本的 dependencies 里的 androidx.compose.material3:material3 或 compose BOM；读出版本号；用 BOM 的按 BOM 映射到 material3 的版本
- 这个版本里 Snackbar 没写的参数的默认值：对应版本库源码的 SnackbarHostState.showSnackbar、SnackbarTokens 和 Snackbar.kt；读 duration 的默认和容器高度、文本内距常量，换成毫秒和 vp。例：卡里那个应用依赖的版本下，单行容器高 48、多行 68，文本垂直内距 6、左右 16
未核实：showSnackbar 的 duration 默认值在库源码里的出处，族里规矩没有核到源码，只有卡里修好验证过的结果
来源：3 张卡，2 个应用
- case-0848ab137044cb92d1bc（Cofi）：做法第 2 步 ← 建议 4
- case-2f11f734c53d33bee770（Cofi）：做法第 2 步 ← 建议 2
- case-d54a9506e30031090325（Jetsnack）：做法第 1 步 ← 建议 6；做法第 2 步 ← 建议 6；做法第 3 步 ← 建议 6

## 规矩

- rule-643e00b84774｜showSnackbar 带 actionLabel 时常驻、无 action 为 4 秒，目标用队列串行展示｜读到：源端 showSnackbar(消息) 不带 actionLabel，或 showSnackbar(消息, actionLabel = …) 带动作，都没写 duration；写错：目标端提示一律按同一时长定时消失，或带动作的提示也被 setTimeout 自动关掉，没有和源端调用对应
- rule-41b6e7fa6ebb｜源端只有一个 SnackbarHost 时，目标用一份反馈状态驱动唯一的底部浮层，新提示替换旧提示｜读到：源端 Scaffold 里只有一个 SnackbarHost(hostState = …)，各操作的结果都调 showSnackbar(…) 显示；写错：目标页 build() 里有多个各自条件渲染的底部浮层（每种结果一个分支、各配定时器），互不排斥，可以同时出现；新提示出现时不清旧的成功状态
- rule-d0d88389cc1b｜自定义组件委托 material3 Snackbar 时，几何按库的 SnackbarTokens 取值｜读到：自定义组件直接调用 `androidx.compose.material3.Snackbar`，只覆盖 shape、几种颜色和 `actionOnNewLine`；写错：目标自绘 Snackbar 写死带库出处注释的常量（单一 `minHeight` 48、文本垂直内距 14），没有多行高度和左右内距
- rule-2e7f26f6d140｜showSnackbar 带动作、关闭钮或读结果时，目标自绘 Snackbar，不用 showToast｜读到：SnackbarHostState.showSnackbar(message, actionLabel, withDismissAction, duration) 的 actionLabel 非空、withDismissAction = true，或调用方比较返回值 == SnackbarResult.ActionPerformed；写错：目标提示出口只有 getPromptAction().showToast(...)，没有动作钮、关闭 X 和结果回传，注释写「Toast 无动作位」
- rule-072b0d72717f｜源端 ActionPerformed 后才执行动作时，目标等 Snackbar 结果，不用 Toast 加确认弹窗代替｜读到：showSnackbar(message, actionLabel, true, SnackbarDuration.Long) == SnackbarResult.ActionPerformed 时才执行动作；写错：目标写成 showToast 或提示组件 show(...) 再加 showAlertDialog 确认弹窗承接动作，注释写「Snackbar 动作按钮 → Toast + 确认弹窗」

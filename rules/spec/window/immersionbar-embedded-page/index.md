# 嵌入页里的 ImmersionBar 沉浸调用

agent 会看到什么：源嵌入页（Fragment 等）里有 ImmersionBar.with(this).statusBarView / titleBarMarginTop、fitsSystemWindows 这类沉浸调用或状态栏占位 View，规格按 page_type=sub_component 写 needs_immersive_safearea=false，或写「由宿主统一处理安全区」

## 规矩

- rule-75e58a90324c｜源码有 ImmersionBar 等沉浸调用时，页面规格按源码判定需要沉浸，不按 page_type 推断｜读到：源码有 `ImmersionBar.with(this).titleBarMarginTop(...)`、`fitsSystemWindows` 等沉浸调用；写错：页面规格按 `page_type=sub_component` 自动写 `needs_immersive_safearea=false`，「沉浸式 + 安全区」节写成 converter 跳过本契约
- rule-64cf244edc6c｜嵌入页有状态栏占位 View 时，规格写明背景延伸到窗口顶、只有前景列避让状态栏｜读到：源嵌入页（Fragment 等）布局里头图背景和一个占位 View 都 app:layout_constraintTop_toTopOf="parent"，内容容器 layout_constraintTop_toBottomOf 该占位；代码里 ImmersionBar.with(this).statusBarView(占位) 把占位撑成状态栏高度；写错：规格把占位 View 写成「Android 沉浸式定位锚点，鸿蒙由宿主统一处理安全区」，安全区节写「由承载本页的宿主负责」；没写背景延伸、前景避让的分层，也没写避让值由谁提供、页内哪一层消费

# 源端 edge-to-edge 下自绘 CAB 时，CAB 期间状态栏区铺 status guard、隐藏工具栏投影

审的是：代码
触发（任一种）：
- 读到：页面用 ActionMode.Callback 显示多选 CAB 覆盖 Toolbar，应用 targetSdk ≥ 35（edge-to-edge 强制）；写错的样子：自绘 CAB 栏只是一行 Row 盖在工具栏上，CAB 期间状态栏区没有 status guard 色块，工具栏投影仍露出；或注释写「CAB 不覆盖状态栏区」
适用范围：源端在 edge-to-edge 下用 AppCompat ActionMode 显示 CAB，目标自绘 CAB 时
做法：
- CAB 显示期间在状态栏区铺 status guard 色块（深色状态栏时为黑色 #ff000000），同时隐藏工具栏投影；CAB 结束后撤掉
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- abc_decor_view_status_guard = #ff000000；abc_decor_view_status_guard_light = #ffffffff：AppCompat status guard 的深色与浅色两种颜色（出处：androidx.appcompat:appcompat 包内 res/values/values.xml，abc_decor_view_status_guard（按应用依赖的版本））
- 框架版按 SYSTEM_UI_FLAG_LIGHT_STATUS_BAR 选色：浅色状态栏用 decor_view_status_guard_light，否则用 decor_view_status_guard：两种颜色怎么选（出处：com.android.internal.policy.DecorView#updateStatusGuardColor）
- targetSdk 为 VANILLA_ICE_CREAM（35）及以上的应用默认强制 edge-to-edge；BAKLAVA（36）及以上 opt-out 属性被忽略：edge-to-edge 成立的条件（出处：Android SDK 平台资源 data/res/values/attrs.xml，windowOptOutEdgeToEdgeEnforcement（按应用的 compileSdk 取对应平台））
- CAB 期间显示黑色 status guard 并隐藏工具栏投影后，与源端对照一致：status guard 的做法（出处：卡里修好并验证过）
针对本应用要查的：
- 源端是否处在 edge-to-edge 下：源工程模块 Gradle 构建脚本里的 targetSdk，主题 XML 里的 android:windowOptOutEdgeToEdgeEnforcement，以及 Activity 里的 enableEdgeToEdge / setDecorFitsSystemWindows 调用；targetSdk ≥ 35 且未 opt out，或 targetSdk ≥ 36，或代码里主动开启了 edge-to-edge，就按 status guard 处理
未核实：AppCompat 的 status guard 逻辑在 AppCompatDelegateImpl，本机只有编译产物，选色规则按框架 DecorView 核对
来源：1 张卡，1 个应用
- case-ccade488607d58d27d0e（omni-notes-hmos）：做法第 1 步 ← 建议 4、诊断；取值 4 ← 诊断

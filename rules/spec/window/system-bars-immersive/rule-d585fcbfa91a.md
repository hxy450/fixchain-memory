# 源 targetSdk≥35 时，规格登记强制 edge-to-edge，分页按源布局是否处理 insets 定避让

审的是：规格
触发（任一种）：
- 读到：Android 构建配置的 targetSdkVersion（含 gradle.properties 里的间接值）≥ 35；页面布局根 android:fitsSystemWindows="false" 或没有 WindowInsets 处理，Toolbar 叠放在内容上；写错的样子：规格全局约定没登记 targetSdk / edge-to-edge 前提，分页规格一律写「内容延伸系统栏 + 前景避让」，把自 y=0 起的 Toolbar 写成需要避让；或只凭 values-v21 的 statusBarColor / colorPrimaryDark 推断状态栏是不透明着色
适用范围：规格提取时为全屏页（含 Toolbar 叠放、自绘 ActionBar 的页面）决定系统栏避让和状态栏外观
做法：
- 先读 targetSdkVersion；≥ 35 时在规格全局约定写一条：「源端强制 edge-to-edge：statusBarColor 失效，无 insets 处理的视图自 y=0 起位于透明状态栏下」
- 分页规格按源布局定避让：fitsSystemWindows=false 或无 WindowInsets 处理的页写「Toolbar / 内容置于 y=0，不做前景避让」，只有确有 insets 处理生效的页才写前景避让
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- ENFORCE_EDGE_TO_EDGE：@EnabledSince(targetSdkVersion = VANILLA_ICE_CREAM)，target SDK 达到即默认 edge-to-edge：强制 edge-to-edge 按应用的 targetSdk 开启（出处：com.android.internal.policy.PhoneWindow#ENFORCE_EDGE_TO_EDGE）
- Build.VERSION_CODES.VANILLA_ICE_CREAM = 35：门槛是 targetSdk 35（出处：android.os.Build.VERSION_CODES#VANILLA_ICE_CREAM）
- targetSdk ≥ VANILLA_ICE_CREAM 时 setStatusBarColor 的颜色是透明且不能改：values-v21 里的 statusBarColor / colorPrimaryDark 不再决定状态栏外观（出处：android.view.Window#setStatusBarColor）
- targetSdk ≥ VANILLA_ICE_CREAM 时 setDecorFitsSystemWindows 的行为等同 false 且不能改：框架不再替内容让出系统栏，没处理 insets 的视图从 y=0 起（出处：android.view.Window#setDecorFitsSystemWindows）
- 参照机实测推翻「fitsSystemWindows 以内边距让出状态栏」；返修把 Toolbar 置 y=0、Web 全屏，去掉状态栏色条：按源布局不避让才和源端一致（出处：卡里修好并验证过）
针对本应用要查的：
- 源应用的 targetSdkVersion：源工程 app 模块的 Gradle 构建脚本（Groovy 或 Kotlin DSL）里的 targetSdk / targetSdkVersion；引用的是变量时去 gradle.properties 或版本目录里按变量名找；读出数字，≥ 35 即强制 edge-to-edge；例：targetSdk 写成某个属性名时，以 gradle.properties 里那一项的值为准
来源：1 张卡，1 个应用
- case-0a77d32c850d4767a2d4（omni-notes-hmos）：做法第 1 步 ← 建议 1、建议 3；做法第 2 步 ← 建议 1、建议 2；取值 5 ← 诊断

# 规格的导航、显隐类验收条目要附转场契约：资源、时长、插值器、起止、覆盖关系

审的是：规格
触发（任一种）：
- 读到：源码进入详情、覆盖页面或显隐时有 setCustomAnimations、startAnimation、res/anim 资源、config_mediumAnimTime 等时长；或页面级 UI spec 写「动画对齐 animateTransition(…)」；写错的样子：feature 规格的导航、显隐类 AC 只写路由等价（「→ navPathStack 路由」「…等价」）或「隐藏」，没有源动画资源、时长、插值器、起止状态和谁覆盖谁
适用范围：规格提取阶段写导航、页面覆盖、行显隐这类验收条目时
做法：
- 每条导航或显隐 AC 附一份转场契约：源动画资源名、时长（解析成毫秒数）、插值器、起止状态（alpha、scale 起止值）、谁覆盖谁，以及显隐是否在动画结束时才切
- 页面级 UI spec 已写「动画对齐 animateTransition」时，也在 feature AC 里写成上面这样可验收的条目，不只引用一句
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- config_shortAnimTime = 200、config_mediumAnimTime = 400、config_longAnimTime = 500（毫秒）：源端时长引 @android:integer/config_*AnimTime 时写进契约的毫秒数（出处：Android SDK 平台资源 data/res/values/config.xml，config_mediumAnimTime（按应用的 compileSdk 取对应平台））
- @android:anim/fade_in：alpha 0.0→1.0，interpolator @interpolator/decelerate_quad，duration @android:integer/config_longAnimTime：源端引平台自带淡入时契约里的起止、插值器和时长（出处：Android SDK 平台资源 data/res/anim/fade_in.xml，fade_in（按应用的 compileSdk 取对应平台））
针对本应用要查的：
- 每段转场的资源、时长、插值器和起止值：源工程 res/anim、res/animator 下被 setCustomAnimations、startAnimation、AnimationUtils.loadAnimation 引用的 XML，以及动画辅助类里的时长常量；资源名照写；android:duration 是数就照写，引 @android:integer/config_* 的按平台 config.xml 解析；from/to 值写成起止状态
来源：1 张卡，1 个应用
- case-298a11d6f7705b3a9362（omni-notes-hmos）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3

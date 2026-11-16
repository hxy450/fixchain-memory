# 建主题文字色令牌前先查 SDK，不把近似值或旧注释里的「平台默认」写进共享 color.json

审的是：资源
触发（任一种）：
- 读到：源 styles 父链止于 android:Theme.Holo 等平台主题，文字色由平台提供；写错的样子：resources/base/element/color.json 里新建的主题文字色令牌是半透明白（#B3FFFFFF、#80FFFFFF）、纯白或记忆中的灰值，「待核」只写在报告里
- 读到：待删组件或旧代码的头注写着某色是「平台默认」（如「Holo 暗色默认 TextView 前景」），没有 SDK 出处；写错的样子：收尾时照头注里的值在 color.json 新建颜色键，或把页面改用这个新键
适用范围：目标工程把平台主题文字色建成 color.json 共享令牌时，含收尾、组件收敛阶段迁回颜色
做法：
- 写令牌前在本机 Android SDK 平台资源里解析到值（themes 的 textColorPrimary / Secondary / Hint → color/ selector → values/colors_holo.xml），按解析值写；查过 SDK 仍取不到才标待核
- 注释里的「平台默认」不算出处：先在 SDK 中核对（如 Widget.TextView → textAppearanceSmall → textColorSecondary），核不到就登记差异，不当场固化成新令牌
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Holo 暗色：主色 #FFF3F3F3、次色 #FFBEBEBE、提示色 #FF808080：修好后 color.json 里三个令牌的值（出处：卡里修好并验证过）
- bright_foreground_holo_dark = @color/background_holo_light = #fff3f3f3；dim_foreground_holo_dark = #bebebe；hint_foreground_holo_dark = #808080：三色在 SDK 里的出处（出处：Android SDK 平台资源 data/res/values/colors_holo.xml，bright_foreground_holo_dark 等（按应用的 compileSdk 取对应平台））
针对本应用要查的：
- 应用实际用的平台主题和 compileSdk：源工程 res/values*/styles.xml 的 parent 链和模块构建脚本里的 compileSdk；到对应 platforms/android-<compileSdk>/data/res 下解析；Holo 以外的主题看 themes_material.xml、themes_device_defaults.xml 里同名条目
来源：1 张卡，1 个应用
- case-e6fd5f0c4d37710c1d97（Blockinger）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 4；取值 1 ← 诊断

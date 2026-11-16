# 平台主题下的文字控件按来源分别取主/次/提示色，显式 @android:color/white 不绑主题主色令牌

审的是：代码
触发（任一种）：
- 读到：源 styles 父链止于 android:Theme.Holo 等平台主题；TextView 只写 textAppearanceLarge / Small 或不写颜色，EditText 没写 textColorHint，另有 TextView 显式 android:textColor="@android:color/white"；写错的样子：目标 Text 一律用主色令牌（或默认未设色的 TextView 取 textColorPrimary）；显式白的 Text 也绑到主题主色令牌 $r('app.color.…_primary') 上
适用范围：把颜色来自 Android 平台主题的文字控件迁成 ArkUI Text / TextInput 时
做法：
- textAppearanceLarge / Medium 的 Text 用主色令牌；textAppearanceSmall，以及既无 textColor 也无 textAppearance 的 TextView 用次色令牌；EditText 没写 textColorHint 时 placeholderColor 用提示色令牌
- 源端显式写的 @android:color/white 写 .fontColor(Color.White) 或单独的键，不绑到主题主色令牌上
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Widget.TextView：textAppearance = ?attr/textAppearanceSmall；TextAppearance.Small：textColor = ?textColorSecondary：未设色的 TextView 取次色，不是主色（出处：Android SDK 平台资源 data/res/values/styles.xml，Widget.TextView、TextAppearance.Small（按应用的 compileSdk 取对应平台））
- @android:color/white = #ffffffff：显式白，和 Holo 暗色主色 #F3F3F3 不同（出处：Android SDK 平台资源 data/res/values/colors.xml，white（按应用的 compileSdk 取对应平台））
- Color.White：ArkUI 的白色枚举（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，Color.White）
- 主色令牌改成 #F3F3F3 后，显式白的文字要脱离主题令牌改用 Color.White：两者分开才都对（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-e6fd5f0c4d37710c1d97（Blockinger）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2、诊断；取值 4 ← 诊断

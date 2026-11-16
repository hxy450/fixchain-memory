# 规格给框架主题的勾选框写转换决策时，形态约束和外观来源分开写，组件栏不直接写 Checkbox

审的是：规格
触发（任一种）：
- 读到：源端 CheckBoxPreference / CheckBox 的勾选图由框架主题提供（平台 drawable btn_checkbox_checked_mtrl / btn_checkbox_unchecked_mtrl）；写错的样子：转换表写「CheckBoxPreference | Checkbox（勾选框，非 Switch/Toggle）」，只写了形态，没写外观来源；实现者把它读成指定 ArkUI Checkbox 组件
适用范围：规格提取阶段为框架主题提供的勾选框写转换决策和验收条目时
做法：
- 形态约束单独一句（是复选框，不是 Switch / Toggle）；外观来源另写：SDK drawable 名、画布 32dp 与方框 18dp、各状态 tint 的解析色
- ArkUI 组件一栏不直接写 Checkbox，写「平台两态图按 checked 切换」
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- btn_checkbox_checked_mtrl：android:width="32dp"、android:viewportWidth="48"，根上 android:tint="@color/control_checkable_material"：规格里要写的外观来源（出处：Android SDK 平台资源 data/res/drawable/btn_checkbox_checked_mtrl.xml（按应用的 compileSdk 取对应平台））
针对本应用要查的：
- 各状态 tint 的解析色：源工程主题 XML 沿 parent 链，没覆盖时到 Android SDK 平台资源 values/themes_material.xml；checked 取 colorControlActivated（→ colorAccent），unchecked 取 colorControlNormal（→ textColorSecondary），解析到具体颜色写进规格
来源：1 张卡，1 个应用
- case-cec44d314b1979a41843（Sokoban）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3、诊断

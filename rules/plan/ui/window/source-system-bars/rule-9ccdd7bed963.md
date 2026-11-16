# 源窗口非全屏时，UI 清单和派工不把各页标成沉浸式、不派四层避让

审的是：计划与派工
触发（任一种）：
- 读到：源主题非全屏（Theme.Holo 等），代码只有 requestWindowFeature(FEATURE_NO_TITLE)，没有任何全屏或透明系统栏标志；写错的样子：UI 清单写「各页全部 needs_immersive_safearea=true」「FEATURE_NO_TITLE → 无标题全屏」，派工写「needs_immersive_safearea: true → 调 Skill(arkts-immersive-safearea) 实施四层架构」和底部安全区任务
适用范围：主会话写 UI 清单、给页面转换派工时决定窗口与避让任务
做法：
- 按源窗口信号逐页定 needs_immersive_safearea；全都没有时写 false 和「非全屏窗口，系统栏照源着色，页面不做 inset 避让」，派工里不派四层架构、WindowModel 和底部安全区
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 清单与派工按 true 下发后，各页都做了不该有的上下避让；还原为非全屏后删除 WindowModel 和各页避让 padding：清单的默认值会被逐页照做（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-af09311d7897ca1af0cd（Blockinger）：做法第 1 步 ← 建议 1、诊断；取值 1 ← 诊断

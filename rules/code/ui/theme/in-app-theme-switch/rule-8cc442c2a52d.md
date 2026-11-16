# 系统栏内容色按生效的 colorMode 计算（亮 #000000 / 暗 #FFFFFF），并在配置变化时重设

审的是：代码
触发（任一种）：
- 读到：源应用 styles.xml 里有浅色 / 深色 / 纯黑几套主题，换主题时状态栏图标随主题变；写错的样子：setWindowSystemBarProperties({ statusBarContentColor: '#000000', navigationBarContentColor: '#000000' }) 写死一个颜色，注释写「深色模式由主题管线后续处理」
适用范围：沉浸式窗口设置系统栏内容色、应用支持深浅色切换时
做法：
- 保存 mainWindow，写 applySystemBarContentColor(mode)：亮色时 statusBarContentColor / navigationBarContentColor 设 '#000000'，暗色时设 '#FFFFFF'，经 mainWindow.setWindowSystemBarProperties(...) 生效
- 在 UIAbility 的 onConfigurationUpdate(newConfig) 和应用内切换主题后都调用一次，按生效的 colorMode 重设
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- setWindowSystemBarProperties(systemBarProperties: SystemBarProperties): Promise<void>：设置系统栏属性（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.setWindowSystemBarProperties）
- SystemBarProperties.statusBarContentColor?: string；navigationBarContentColor?: string：状态栏、导航栏的内容色（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，SystemBarProperties）
- onConfigurationUpdate(newConfig: Configuration): void：系统配置（含颜色模式）变化时回调（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.Ability.d.ts，Ability.onConfigurationUpdate）
- 内容色改成按 mode 计算并在 onConfigurationUpdate 里重设后，深色下系统栏图标可见：验证过的写法（出处：卡里修好并验证过）
- onConfigurationUpdate(newConfig: Configuration): void：同族接口：AbilityStage 上的配置变化回调（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.AbilityStage.d.ts，AbilityStage.onConfigurationUpdate）
来源：1 张卡，1 个应用
- case-e1b1f9786e31a8d527cc（AntennaPod）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3；取值 4 ← 诊断

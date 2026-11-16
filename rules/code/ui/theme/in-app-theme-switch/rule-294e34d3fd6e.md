# 应用内用 setColorMode 切主题时，命令式取色改用覆写 colorMode 的资源管理器

审的是：代码
触发（任一种）：
- 读到：源端换主题靠 Activity 重建（ActivityCompat.recreate / Activity.recreate），主题在界面创建时按用户偏好 setTheme；写错的样子：目标端只调用 ApplicationContext.setColorMode，注释断言「全部 $r 资源随 mode 即时重解析，等价 recreate」；画布、HTML 样式等仍用 context.resourceManager.getColorSync 取色，应用内选深色而系统为浅色时取到浅色值
适用范围：应用内深浅色切换迁成 setColorMode、且有在代码里命令式取色的消费点（Canvas、Web 内联 CSS、getColorSync）时
做法：
- 先在工程里搜 getColorSync / getColor、Canvas 的 strokeStyle / fillStyle、HTML/CSS 内联色、setWindowSystemBarProperties，逐类写明切换后由谁重解析
- 主题控制器统一导出按当前主题覆写的资源管理器：const cfg = rm.getOverrideConfiguration(); cfg.colorMode = 深色 ? resourceManager.ColorMode.DARK : resourceManager.ColorMode.LIGHT; const themedRm = rm.getOverrideResourceManager(cfg)；画布、HTML 样式等取色点改用 themedRm
- 取色点订阅主题状态或 onConfigurationUpdate，变化时重新取色并重绘
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- setColorMode(colorMode: ConfigurationConstant.ColorMode): void（ApplicationContext，@since 18 的说明：只能在主线程调用）：设置应用的颜色模式（出处：鸿蒙 SDK 的 ets/api/application/ApplicationContext.d.ts，ApplicationContext.setColorMode）
- getOverrideResourceManager(configuration?: Configuration): ResourceManager；getOverrideConfiguration(): Configuration：按指定配置取资源的资源管理器（@since 12）（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，ResourceManager.getOverrideResourceManager / getOverrideConfiguration）
- Configuration.colorMode: ColorMode；ColorMode.DARK = 0，ColorMode.LIGHT = 1：覆写配置里要改的字段和取值（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，Configuration.colorMode、ColorMode）
- getColorSync(resId: number): number：命令式取色，返回数值颜色（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，ResourceManager.getColorSync）
- 限定词目录匹配只能筛出最匹配的资源；要取指定配置的资源，用 getOverrideResourceManager：文档给的取指定配置资源的办法（出处：resource-categories-and-access.md，获取指定配置的资源）
- 应用内选深色、系统为浅色时 context.resourceManager.getColorSync 仍返回浅色值；改用覆写 colorMode 的资源管理器后正确：setColorMode 不会改 context.resourceManager 的取色结果（出处：卡里修好并验证过）
- Activity.recreate：用新实例重建 Activity，流程同配置变化时的重建：源端换主题时构造期取色会整体重做，目标端要自己补重解析（出处：android.app.Activity#recreate）
未核实：卡里没查到平台文档说明 setColorMode 和 context.resourceManager 的关系，「getColorSync 仍按设备配置解析」出自返修真机实测
来源：1 张卡，1 个应用
- case-e1b1f9786e31a8d527cc（AntennaPod）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 2、诊断；做法第 3 步 ← 建议 2；取值 6 ← 诊断

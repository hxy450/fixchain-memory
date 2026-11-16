# 偏好存储换上下文前先核对两种 Context 的 preferencesDir，不以「可靠」为理由

审的是：代码
触发（任一种）：
- 写错的样子：修复把 preferences 的 context 从 getApplicationContext() 换成 UIAbilityContext（this.context），理由写「applicationContext 持久化不如 UIAbilityContext 可靠」
适用范围：修复阶段更换首选项或其他沙箱文件所用的上下文时
做法：
- 换之前按文档核对两种上下文的 preferencesDir 是否相同：ApplicationContext 是应用级的 base/preferences，UIAbilityContext、AbilityStageContext 是模块级的 base/haps/<module-name>/preferences，不是同一个文件
- 修复理由写查到的数据位置，不写没有平台依据的「可靠性」；位置不同时写明此前经另一种上下文写入的数据在哪
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- preferencesDir：ApplicationContext 是 <路径前缀>/<加密等级>/base/preferences；AbilityStageContext、UIAbilityContext、ExtensionContext 是 <路径前缀>/<加密等级>/base/haps/<module-name>/preferences：应用级和模块级上下文的首选项目录不同（出处：application-context-stage.md，获取应用文件路径（表1））
- 用户首选项的持久化文件存储在preferencesDir路径下：首选项文件跟着传入的 context 的 preferencesDir 走（出处：js-apis-data-preferences.md，开头说明）
未核实：两种上下文写入的数据冷启动后能否读回，卡里没有上机验证
来源：1 张卡，1 个应用
- case-f93cb4842b050b7fb269（polypal-app-ohos）：做法第 1 步 ← 建议 4；做法第 2 步 ← 建议 4

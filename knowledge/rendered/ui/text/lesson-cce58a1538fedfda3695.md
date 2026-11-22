# 源端 textAllCaps（含 Material、AppCompat、MaterialComponents 主题下 Button 与 AlertDialog 按钮样式默认的全大写；Holo 与 Material3 主题的按钮默认不全大写）必须显示为全大写，按资源原样不是可接受的降级：取资源字符串后按当前 locale toLocaleUpperCase（Resource 参数先 getStringSync），封装成共享 allCaps 复用；textCase(UpperCase) 只转拉丁字母，不用它代替

## 何时使用

界面实现或返修阶段，把安卓 textAllCaps（含按钮样式默认的全大写）移植为 ArkUI 文本，确定取字符串方式与 locale 标签，或给多个页面的按钮统一做大小写变换时

## 适用情境

安卓按钮或文本靠 textAllCaps（AllCapsTransformationMethod 按当前 locale 大写）显示全大写，资源串多为首字母大写（Yes/No、New Game）；应用带含非 ASCII 或非拉丁字母的多语言资源（de 的 ü、tr 的 i/İ、ru 的西里尔字母），也可能以只有语言码的应用偏好语言运行；目标按钮参数常是 Resource/ResourceStr，要自己取字符串做大写，并把 resourceManager 配置的 locale（下划线分隔、子标签可能为空，如 fa_Arab_）转成 BCP 47 标签。也包括工程里已有按 locale 大写的私有实现，其他页面又用 textCase 另写一套。

## 原因

来源观察到 ArkUI textCase(TextCase.UpperCase) 没有把 ü 与西里尔字母转成大写，与安卓按 locale 的大写不一致；但这只说明 textCase 不准，不是保留资源原样的理由——另一来源中写者因参数是 ResourceStr、textCase 又被禁止，就放弃了大写。改用 toLocaleUpperCase 后，直接传资源 locale 会抛 RangeError；按单个样本（en_Latn_US）把下划线换成连字符，又会在子标签为空的 locale 下生成非法标签而崩溃。同一工程两套做法并存、只按英文截图验收时，非拉丁语言下的差异会漏掉。

## 做法

1. 按钮或文本参数是 Resource/ResourceStr 时，先经 resourceManager.getStringSync（或 UIContext 宿主 context 的资源管理器）取字符串，再调用 toLocaleUpperCase(tag)，与 AllCapsTransformationMethod 的 toUpperCase(locale) 对齐；封装为共享 allCaps(ctx, text)，语言切换后重算。写跨页文字变换前先 grep 工程已有实现并复用，不另写一套。
2. tag 由资源配置 locale 按 '_' 拆分、丢弃空子标签、再用 '-' 连接；结果为空或调用抛 RangeError 时回落到不带 locale 的 toUpperCase()。

## 可选检查

- 写完后在一种含非 ASCII 字母的资源语言（如 de）、一种非拉丁资源语言（如 ru）与只有语言码的应用偏好语言（如 fa）下各看一次显示，并确认 faultlog 没有新增 jscrash。

来源支持：3 张卡 · 2 次迁移 · 2 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；安卓 Android SDK 平台资源 android-34；Android SDK 源码 android-36.1；appcompat 1.7.1。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境〕AllCapsTransformationMethod.getTransformation：locale 取 TextView.getTextLocale()，取不到用构造时的 getResources().getConfiguration().getLocales().get(0)，再 TextUtils.toUpperCase(locale, source, copySpans)
- 〔适用情境〕按钮默认全大写（按钮样式或控件没有另设 textAllCaps=false 时）：TextAppearance.Material.Button、Base.TextAppearance.AppCompat.Button 都写 textAllCaps=true；AlertDialog 按钮的 buttonBarButtonStyle（Widget.Material.Button.ButtonBar.AlertDialog / Widget.AppCompat.Button.ButtonBar.AlertDialog）经 Borderless.Colored 的文字外观继承到它们，同样全大写
- 〔做法第 1 步〕ResourceManager.getStringSync(resId: number): string 可用；getStringSync(resource: Resource) 自 API 20 @deprecated（useinstead getStringSync），可传 resource.id（Resource.id: number）
- 〔做法第 1 步〕UIContext.getHostContext(): Context | undefined，返回的宿主 Context 带 resourceManager
- 〔做法第 1 步〕textCase(value: TextCase) 在 TextAttribute 与 SpanAttribute 上；TextCase 只有 Normal、LowerCase、UpperCase，声明没说明 locale 与非 ASCII 字母的处理
- 〔做法第 1 步〕textCase(TextCase.UpperCase) 在设备上只转部分字母：德语 ü 仍是小写（安卓 textAllCaps 为 Ü），西里尔字母不转；String.toLocaleUpperCase 传德语、俄语标签时这些字母都正常大写
- 〔做法第 1 步〕语言切换的通知：Ability.onConfigurationUpdate(newConfig: Configuration)，或 ApplicationContext.on('environment', EnvironmentCallback) 的 onConfigurationUpdated(config)；Configuration.language?: string
- 〔做法第 2 步〕ResourceManager.getConfigurationSync(): Configuration；Configuration.locale: string（@since 12）；目标端 String.prototype.toLocaleUpperCase(locales?: string | string[])
- 〔做法第 2 步〕设备上 ResourceManager.getConfigurationSync().locale 为下划线分隔：en_Latn_US；应用偏好语言只有语言码时为 fa_Arab_（尾部空子标签）。把它原样或只把 _ 换成 -（得到 fa-Arab-）传给 toLocaleUpperCase 是非法标签，抛 RangeError、应用崩溃。声明注释里的示例 zh-Hans-CN 为连字符写法

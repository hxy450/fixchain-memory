# 源端 textAllCaps（含 Material、AppCompat、MaterialComponents 主题下 Button 与 AlertDialog 按钮样式默认的全大写；Holo 与 Material3 主题的按钮默认不全大写）必须显示为全大写，按资源原样不是可接受的降级：取资源字符串后按当前 locale toLocaleUpperCase（Resource 参数先 getStringSync），封装成共享 allCaps 复用；textCase(UpperCase) 不转 ü、西里尔字母这类非 ASCII 字母，不用它代替

## 何时使用

界面实现或返修阶段，把安卓 textAllCaps（含按钮样式默认的全大写）移植为 ArkUI 文本，确定取字符串方式与 locale 标签，或给多个页面的按钮统一做大小写变换时

## 适用情境

安卓按钮或文本靠 textAllCaps（AllCapsTransformationMethod 按当前 locale 大写）显示全大写，资源串多为首字母大写（Yes/No、New Game）；应用带含非 ASCII 或非拉丁字母的多语言资源（de 的 ü、tr 的 i/İ、ru 的西里尔字母），也可能以只有语言码的应用偏好语言运行；目标按钮参数常是 Resource/ResourceStr，要自己取字符串做大写，并把 resourceManager 配置的 locale（下划线分隔、子标签可能为空，如 fa_Arab_）转成 BCP 47 标签。也包括工程里已有按 locale 大写的私有实现，其他页面又用 textCase 另写一套。

## 原因

来源观察到 ArkUI textCase(TextCase.UpperCase) 没有把 ü 与西里尔字母转成大写，与安卓按 locale 的大写不一致；但这只说明 textCase 不准，不是保留资源原样的理由——另一来源中写者因参数是 ResourceStr、textCase 又被禁止，就放弃了大写。改用 toLocaleUpperCase 后，直接传资源 locale 会抛 RangeError；按单个样本（en_Latn_US）把下划线换成连字符，又会在子标签为空的 locale 下生成非法标签而崩溃。同一工程两套做法并存、只按英文截图验收时，非拉丁语言下的差异会漏掉。

## 做法

1. 按钮或文本参数是 Resource/ResourceStr 时，先经 resourceManager.getStringSync(资源的 id)（或 UIContext 宿主 context 的资源管理器；传 Resource 对象的重载自 API 20 起废弃）取字符串，再调用 toLocaleUpperCase(tag)，与 AllCapsTransformationMethod 的 toUpperCase(locale) 对齐；封装为共享 allCaps(ctx, text)，语言切换后重算。写跨页文字变换前先 grep 工程已有实现并复用，不另写一套。
2. tag 由资源配置 locale 按 '_' 拆分、丢弃空子标签、再用 '-' 连接；结果为空或调用抛 RangeError 时回落到不带 locale 的 toUpperCase()。

## 可选检查

- 写完后在一种含非 ASCII 字母的资源语言（如 de）、一种非拉丁资源语言（如 ru）与只有语言码的应用偏好语言（如 fa）下各看一次显示，并确认 faultlog 没有新增 jscrash。

来源支持：3 张卡 · 2 次迁移 · 2 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36 的平台资源（另比对 android-30、33、34、35、37.0）；android-36.1 的源码；androidx.appcompat:appcompat 1.1.0、1.7.1、1.8.0；com.google.android.material:material 1.4.0、1.5.0、1.8.0、1.12.0、1.14.0。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔标题 / 适用情境〕TextView 的 textAllCaps 为 true 时挂 AllCapsTransformationMethod：取 TextView.getTextLocale()（为空时取构造时 Context 配置里的第一个 locale），调 TextUtils.toUpperCase(locale, …) 按该 locale 转大写；文本可选（textIsSelectable）或是可编辑文本（如 EditText）时 TextView 不允许变换改变长度，这个方法原样返回、不转大写
- 〔适用情境〕TextView 构造时先读 textAppearance 里的 textAllCaps，再读控件自身、style= 和默认控件样式（defStyleAttr，如主题的 buttonStyle）上的 android:textAllCaps，后者覆盖前者；这几处都没写 android:textAllCaps 时由 textAppearance 决定，按钮的 textAppearance 多来自主题的 textAppearanceButton；设了密码输入类型时构造最后换成 PasswordTransformationMethod，不再转大写
- 〔标题 / 适用情境〕平台 Material 主题（Theme.Material 及其子主题，android-30 至 37.0 相同）下，应用没有另设按钮样式时：Widget.Material.Button 的 textAppearance 取 ?attr/textAppearanceButton，即 TextAppearance.Material.Widget.Button，其父样式 TextAppearance.Material.Button 设 textAllCaps=true；主题的 buttonBarButtonStyle 为 Widget.Material.Button.ButtonBar.AlertDialog（Light 主题是继承它的 Widget.Material.Light.Button.ButtonBar.AlertDialog），经 Borderless.Colored 的文字样式也落到 TextAppearance.Material.Button，AlertDialog 按钮同样默认全大写；手表（values-watch）里这个对话框按钮样式改继承 Borderless.Small，文字样式回到 textAppearanceButton，仍是全大写
- 〔标题〕平台 Holo 主题下，应用没有另设按钮样式时：Widget.Holo.Button 的 textAppearance 是 ?attr/textAppearanceMedium，主题的 textAppearanceButton 是 TextAppearance.Holo.Widget.Button，两条链上都没有 textAllCaps，按钮文字默认不全大写
- 〔标题〕DeviceDefault 主题的按钮文字样式 TextAppearance.DeviceDefault.Widget.Button 把 textAllCaps 设为 @bool/config_buttonTextAllCaps，android-30 至 37.0 的平台资源里这个值都是 true、没有限定目录变体；应用没有另设按钮样式时按钮文字默认全大写
- 〔标题 / 适用情境〕androidx.appcompat（1.1.0、1.7.1、1.8.0 相同）下，应用没有另设按钮样式时：Theme.AppCompat 系的 android:textAppearanceButton 为 TextAppearance.AppCompat.Widget.Button，链到 Base.TextAppearance.AppCompat.Button——API 21 以下取它自己写的 android:textAllCaps=true，API 21 起 values-v21 把它的父样式换成平台 TextAppearance.Material.Button，取平台的 textAllCaps=true；AlertDialog 按钮样式 Widget.AppCompat.Button.ButtonBar.AlertDialog 经 Base.Widget.AppCompat.Button.Borderless.Colored，API 21 起落到平台 Widget.Material.Button.Borderless.Colored 的文字样式，同样全大写；两种按钮默认全大写
- 〔标题〕com.google.android.material 1.4.0 至 1.14.0 下，应用没有另设按钮样式时：MaterialComponents 主题的 textAppearanceButton 为 TextAppearance.MaterialComponents.Button（其 Base 样式 android:textAllCaps=true），按钮默认全大写；Material3 样式（1.5.0 起才有）里 Widget.Material3.Button、Widget.Material3.Button.TextButton（对话框按钮 TextButton.Dialog 继承它）的 android:textAppearance 在 1.5.0 直接写 ?attr/textAppearanceLabelLarge，1.8.0、1.12.0、1.14.0 经 macro 指向它，都解析到 TextAppearance.Material3.LabelLarge，其 android:textAllCaps 为 false（1.5.0 经 @bool/m3_sys_typescale_label_large_text_all_caps，值为 false），按钮默认不全大写
- 〔标题 / 原因〕Text 的 textCase(value: TextCase) 未设置时为 TextCase.Normal；TextCase.UpperCase 的声明注释和文档只写「文本采用全大写」，没有说明对非 ASCII 字母和 locale 的处理
- 〔标题 / 原因〕HarmonyOS 6.1.0 设备上，Text 设 textCase(TextCase.UpperCase) 时德语资源串显示为 ZURüCKSETZEN（ü 没有转大写，安卓为 ZURÜCKSETZEN），俄语按钮文字只有首字母大写（西里尔字母没有转大写），拉丁 ASCII 字母正常转大写；同一设备上取出资源串再调 toLocaleUpperCase(locale)，德语得到 ZURÜCKSETZEN，俄语西里尔字母也转成大写，与安卓显示相同
- 〔做法第 1 步〕ResourceManager.getStringSync(resId: number) 自 API 9 起提供，同步返回字符串；getStringSync(resource: Resource) 自 API 9 起提供、API 20 起废弃，文档建议改用按资源 ID 的 getStringSync
- 〔做法第 1 步〕UIContext.getHostContext() 返回 Context | undefined（API 12 起），取到的宿主 Context 上有 resourceManager
- 〔做法第 1 步〕系统语言等环境变量变化时会调用 UIAbility.onConfigurationUpdate(newConfig)（AbilityStage、ApplicationContext 的环境回调也会收到），文档说明在其中取最新环境变量而无需重启 UIAbility；Configuration.language 自 API 18 起提供；应用用 ApplicationContext.setLanguage 设了应用语言后，不再收到系统语言变化
- 〔适用情境 / 做法第 2 步〕ResourceManager.getConfigurationSync() 返回的 Configuration.locale 是字符串：声明注释的示例是 zh-Hans-CN（连字符分隔），文档只写「语言文字国家地区」，两处都没写明分隔符和子标签为空的情形；设备上实际取到的是下划线分隔的值（见卡里实测），运行时格式以实测为准
- 〔适用情境 / 做法第 2 步〕HarmonyOS 6.1.0 设备上，resourceManager.getConfigurationSync().locale 取到过 en_Latn_US（下划线分隔）；应用偏好语言只有语言码 fa 时取到 fa_Arab_（末尾子标签为空）
- 〔原因 / 做法第 2 步〕把带下划线的 locale 原样传给 toLocaleUpperCase，或把 fa_Arab_ 只替换下划线得到的 fa-Arab- 传进去时，调用抛 RangeError，应用崩溃，faultlog 记下 jscrash

# 源端 textAllCaps（含 Material、AppCompat、MaterialComponents 主题下 Button 与 AlertDialog 按钮样式默认的全大写；Holo 与 Material3 主题的按钮默认不全大写）必须显示为全大写，按资源原样不是可接受的降级：取资源字符串后按当前 locale toLocaleUpperCase（Resource 参数先 getStringSync），封装成共享 allCaps 复用；textCase(UpperCase) 只转拉丁字母，不用它代替

ID：`lesson-cce58a1538fedfda3695` · 版本：2

> 带知识的试验版（未并入 store）：正文按 `knowledge/lessons/lesson-cce58a1538fedfda3695.json` 改了 1 句，后面接了 14 条已核实的平台事实。原文、来源和证据卡见 [memory/ui/text/lesson-cce58a1538fedfda3695.lesson.md](../../../../memory/ui/text/lesson-cce58a1538fedfda3695.lesson.md)。

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

## 已核实的平台事实

核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；安卓 Android SDK 平台资源 android-34；Android SDK 源码 android-36.1；appcompat 1.7.1。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看；每条下面的「写法」是在 SDK 声明里核过的导入语句、归属、签名和枚举成员，写代码时直接照抄。

- 〔适用情境〕AllCapsTransformationMethod.getTransformation：locale 取 TextView.getTextLocale()，取不到用构造时的 getResources().getConfiguration().getLocales().get(0)，再 TextUtils.toUpperCase(locale, source, copySpans)（出处：android.text.method.AllCapsTransformationMethod#getTransformation、构造函数）
- 〔适用情境〕按钮默认全大写（按钮样式或控件没有另设 textAllCaps=false 时）：TextAppearance.Material.Button、Base.TextAppearance.AppCompat.Button 都写 textAllCaps=true；AlertDialog 按钮的 buttonBarButtonStyle（Widget.Material.Button.ButtonBar.AlertDialog / Widget.AppCompat.Button.ButtonBar.AlertDialog）经 Borderless.Colored 的文字外观继承到它们，同样全大写（出处：Android SDK 平台资源 data/res/values/styles_material.xml，TextAppearance.Material.Button、Widget.Material.Button.ButtonBar.AlertDialog、TextAppearance.Material.Widget.Button.Borderless.Colored；values/themes_material.xml，buttonBarButtonStyle；appcompat 1.7.1 包内 res/values/values.xml、values-v21/values-v21.xml）
- 〔做法第 1 步〕ResourceManager.getStringSync(resId: number): string 可用；getStringSync(resource: Resource) 自 API 20 @deprecated（useinstead getStringSync），可传 resource.id（Resource.id: number）（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，ResourceManager.getStringSync；ets/api/global/resource.d.ts，Resource.id）
  写法：实例：context.resourceManager（Context 的属性，类型 resourceManager.ResourceManager）；写类型时 import { resourceManager } from '@kit.LocalizationKit'
        getStringSync(resId: number): string、getStringSync(resId: number, ...args: Array<string | number>): string；Resource.id: number，如 rm.getStringSync(res.id)
- 〔做法第 1 步〕UIContext.getHostContext(): Context | undefined，返回的宿主 Context 带 resourceManager（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，UIContext.getHostContext）
  写法：组件内 this.getUIContext() 得到 UIContext（BaseCustomComponent.getUIContext(): UIContext）
        uiContext.getHostContext(): Context | undefined（@since 12，仅 Stage 模型），再取 .resourceManager；类型导入 import { UIContext } from '@kit.ArkUI'、import { common } from '@kit.AbilityKit'（common.Context）
- 〔做法第 1 步〕textCase(value: TextCase) 在 TextAttribute 与 SpanAttribute 上；TextCase 只有 Normal、LowerCase、UpperCase，声明没说明 locale 与非 ASCII 字母的处理（出处：鸿蒙 SDK 的 ets/component/text.d.ts，TextAttribute.textCase；ets/component/span.d.ts，SpanAttribute.textCase；ets/component/enums.d.ts，TextCase）
  写法：Text、Span：.textCase(value: TextCase)；TextCase { Normal, LowerCase, UpperCase } 全局枚举，不用导入
- 〔做法第 1 步〕textCase(TextCase.UpperCase) 在设备上只转部分字母：德语 ü 仍是小写（安卓 textAllCaps 为 Ü），西里尔字母不转；String.toLocaleUpperCase 传德语、俄语标签时这些字母都正常大写（出处：卡里上机实测（case-4f8a6d24236bd7f92a26、case-742668c1933f26d6bff9））
  写法：目标字符串方法：str.toLocaleUpperCase(locales?: string | string[]): string；textCase 签名见 textCase 条
- 〔做法第 1 步〕语言切换的通知：Ability.onConfigurationUpdate(newConfig: Configuration)，或 ApplicationContext.on('environment', EnvironmentCallback) 的 onConfigurationUpdated(config)；Configuration.language?: string（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.Ability.d.ts，onConfigurationUpdate；ets/api/application/ApplicationContext.d.ts，on('environment')；ets/api/@ohos.app.ability.EnvironmentCallback.d.ts；ets/api/@ohos.app.ability.Configuration.d.ts，language）
  写法：import { UIAbility, Configuration, EnvironmentCallback, AbilityConstant } from '@kit.AbilityKit'
        UIAbility 子类覆写 onConfigurationUpdate(newConfig: Configuration): void；或 context.getApplicationContext().on('environment', callback: EnvironmentCallback): number，取消用 off('environment', callbackId: number): Promise<void>
        EnvironmentCallback { onConfigurationUpdated(config: Configuration): void; onMemoryLevel(level: AbilityConstant.MemoryLevel): void }；这里的 Configuration 来自 AbilityKit（含 language?: string），与 resourceManager.Configuration 不是同一个类型
- 〔做法第 2 步〕ResourceManager.getConfigurationSync(): Configuration；Configuration.locale: string（@since 12）；目标端 String.prototype.toLocaleUpperCase(locales?: string | string[])（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，ResourceManager.getConfigurationSync、Configuration.locale；ets/build-tools/ets-loader/bin/ark/build-win/aot/src/lib_ark_builtins.d.ts，String.toLocaleUpperCase）
  写法：resourceManager.Configuration { direction: Direction; locale: string; deviceType: DeviceType; screenDensity: ScreenDensity; colorMode: ColorMode; mcc: number; mnc: number }
        调用 context.resourceManager.getConfigurationSync()；不带 locale 的回落写 str.toUpperCase(): string
- 〔做法第 2 步〕设备上 ResourceManager.getConfigurationSync().locale 为下划线分隔：en_Latn_US；应用偏好语言只有语言码时为 fa_Arab_（尾部空子标签）。把它原样或只把 _ 换成 -（得到 fa-Arab-）传给 toLocaleUpperCase 是非法标签，抛 RangeError、应用崩溃。声明注释里的示例 zh-Hans-CN 为连字符写法（出处：卡里上机实测（case-4f8a6d24236bd7f92a26）；鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，Configuration.locale 注释）
  写法：签名见 getConfigurationSync、toLocaleUpperCase 条
- 〔适用情境〕按钮默认是否全大写取决于主题（按钮和样式都没有另设 textAllCaps 时）：Theme.Holo、Theme.Holo.Light 的 Widget.Holo.Button 文字取 textAppearanceMedium，不全大写；Theme.Material(.Light、.Light.DarkActionBar)、Theme.AppCompat(.Light、.Light.DarkActionBar、.DayNight) 经 TextAppearance.Material.Button 全大写；Theme.MaterialComponents(.Light、.Light.DarkActionBar、.DayNight) 的 MaterialButton 经 Base.TextAppearance.MaterialComponents.Button 全大写；Theme.DeviceDefault 的按钮文字 textAllCaps=@bool/config_buttonTextAllCaps（AOSP 为 true，厂商可覆盖）；Material3 主题的 Widget.Material3.Button 文字取 TextAppearance.M3.Sys.Typescale.LabelLarge，textAllCaps=false（material 1.12.0、1.14.0）。android-30 至 36、appcompat 1.1.0–1.8.0、material 1.4.0–1.14.0 结论相同（出处：Android SDK 平台资源 data/res/values/styles_holo.xml，Widget.Holo.Button、TextAppearance.Holo.Medium；data/res/values/styles_device_defaults.xml，TextAppearance.DeviceDefault.Widget.Button、config_buttonTextAllCaps；data/res/values/config.xml，config_buttonTextAllCaps；com.google.android.material:material 1.4.0、1.12.0、1.14.0 包内 res/values，Widget.MaterialComponents.Button、Base.TextAppearance.MaterialComponents.Button、Widget.Material3.Button、TextAppearance.M3.Sys.Typescale.LabelLarge）
- 〔适用情境〕对话框按钮默认是否全大写（样式没有另设时）：平台 AlertDialog 在 Theme.Holo(.Light) 下按钮为 Widget.Holo(.Light).Button 无全大写；在 Material、DeviceDefault、AppCompat、MaterialComponents 宿主主题下全大写（DeviceDefault 取 config_buttonTextAllCaps）；androidx.appcompat.app.AlertDialog 在 AppCompat、MaterialComponents 主题下全大写，在 Material3 主题下不全大写；MaterialAlertDialogBuilder 在 MaterialComponents 主题下（buttonBarPositiveButtonStyle 链到 Base.TextAppearance.MaterialComponents.Button）全大写，在 Material3 主题下（Widget.Material3.Button.TextButton.Dialog → LabelLarge）不全大写（出处：Android SDK 平台资源 data/res/values/themes_holo.xml，Theme.Holo.Dialog.Alert、buttonBarButtonStyle；data/res/values/styles_material.xml，Widget.Material.Button.ButtonBar.AlertDialog；com.google.android.material:material 1.12.0、1.14.0 包内 res/values，ThemeOverlay.MaterialComponents.MaterialAlertDialog、ThemeOverlay.Material3.MaterialAlertDialog、Widget.Material3.Button.TextButton.Dialog）
- 〔适用情境 / 做法第 1 步〕AppCompatTextView、AppCompatButton 从 textAppearance 读到 textAllCaps 后调用平台 TextView.setAllCaps，走的是平台 AllCapsTransformationMethod（appcompat 1.8.0 的 AppCompatTextHelper#setAllCaps）；appcompat 另有自己的 androidx.appcompat.text.AllCapsTransformationMethod，构造时取 Configuration.locale，变换用 String.toUpperCase(Locale)，与平台版的取 locale 方式不同（出处：androidx.appcompat:appcompat 1.8.0 字节码 widget.AppCompatTextHelper#setAllCaps、text.AllCapsTransformationMethod；android.widget.TextView#setAllCaps）
- 〔做法第 1 步〕平台 AllCapsTransformationMethod 最终调用 TextUtils.toUpperCase(locale, source, copySpans)，内部用 ICU CaseMap.toUpper() 按 locale 做大写：土耳其语、阿塞拜疆语的 i 变 İ，德语 ß 变 SS（结果可能变长，span 按映射平移），希腊语按 ICU 规则去重音；目标 toLocaleUpperCase 传同一语言标签才能对齐这些特例（出处：android.text.TextUtils#toUpperCase；android.text.method.AllCapsTransformationMethod#getTransformation）
- 〔做法第 1 步〕ResourceManager 取字符串的同步、异步与按名版本：getStringSync(resId) / getStringSync(resId, ...args) 同步（带 args 的格式化版 API 10）；getStringValue(resId) 返回 Promise<string>（API 9）；getStringByNameSync(resName)（API 9）按资源名取；Resource 参数的 getStringSync、getStringValue 自 API 20 废弃；配置有 getConfigurationSync()（API 10）与 getConfiguration(): Promise<Configuration>（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，ResourceManager.getStringSync、ResourceManager.getStringValue、ResourceManager.getStringByNameSync、ResourceManager.getConfiguration、ResourceManager.getConfigurationSync）
  写法：import { resourceManager } from '@kit.LocalizationKit';  // 实例：context.resourceManager
        getStringSync(resId: number): string；getStringSync(resId: number, ...args: Array<string | number>): string
        getStringValue(resId: number): Promise<string>；getStringByNameSync(resName: string): string
        getConfigurationSync(): resourceManager.Configuration；getConfiguration(): Promise<resourceManager.Configuration>

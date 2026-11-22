# 字符串语言目录与键集按源端实际存在的 values-<语言>（含依赖库合并资源）镜像：限定词粒度照源，不合成译文，缺键回落 base

## 何时使用

规格提取与资源迁移阶段，确定要迁移哪些 values-* 语言目录及其目标限定词、目标生成哪些语言限定字符串目录及各键取值、源 locale 缺键如何处理时

## 适用情境

Android 源只有默认 res/values/strings.xml（常为英文），没有 values-zh 等语言限定目录；规格要求与源应用逐屏对齐或写明“不擅自翻译”；资源转换 skill 带有“至少生成两套语言、默认英文则补 zh_CN”一类通用规则；设备可能使用中文系统语言。也包括源端有多个 values-xx（如 es/fr/it/pt/ru/zh/zh-rTW）并提供应用内语言切换，规格或主会话却自定“默认只迁 values + values-zh”，并以“项目决策优先”覆盖资源 skill 的“全部转换”硬规则；部分语言目录键集不全，skill 要求键集一致并自动补译。也包括源端只有仅语言限定的 values-zh，skill 正文写“values-zh-rCN 或 values-zh → zh_CN 或 zh”并要求最少生成 zh_CN，而详细映射表写 values-zh→zh、values-zh-rCN→zh_CN。

## 例外与边界

- 规格或决策明确要求本轮新增本地化语言；此时按批准的译文来源生成，并在报告中注明源端没有该语言
- 源端引用 android.R.string.* 等框架字符串：译文由系统按设备语言提供，按系统字符串的经验为已有语言补框架译文（必要时补地区目录）

## 原因

HarmonyOS 在中文系统语言下优先取 zh_CN，合成的中文译文让界面显示中文或中英混排，而同一设备上的 Android 源应用显示默认英文；按键集合一致的检查发现不了取值差异。限定词改粒度同样改变匹配范围：仅语言的 values-zh 在 Android 7.0（API 24）起服务所有简体（推断文字为 Hans）的中文 locale（zh-CN、zh-SG 等，不含 zh-TW、zh-HK），7.0 以前服务所有中文 locale，改写成 zh_CN 后只匹配中国大陆地区，其他中文地区的设备取不到这份译文。缩减语言范围后，应用内选择其他语言只显示英文；为源 locale 缺失的键补写译文，目标会显示源端没有的文案，而 Android 对这些键回落默认 values。只转换应用自身 res/ 时，依赖库随 APK 合并进来的文案（库提供的按钮、选择器与提示文案）以及应用没有、只由库提供的语言目录会整体缺失。

## 做法

1. 先盘点源端实际存在的 `values-<locale>` 目录（values-night、values-sw600dp 等不是语言目录），只为这些语言生成目标限定目录；源只有默认 values/ 时只写 base。工程依赖自带字符串资源的库（appcompat、material、preference、对话框与选择器库）且目标复刻其文案时，盘点范围是构建产物的合并资源表：按资源转换 skill 先构建 APK 再用 apktool 或 aapt2 取合并资源表；构建不了就按 build.gradle 依赖从 Gradle 缓存 AAR 取各库 res/values-*，仍取不到的库资源在映射报告逐项列出。
2. 通用 skill 的默认语言规则与项目规格或源码单语事实冲突时，以规格和源码为准，并在资源映射报告写明冲突与取舍。
3. 流程确需保留第二语言目录（例如只放脚手架的 app/ability 键）时，业务键省略以回落 base，或取值与 base 完全一致。
4. 按源 res 下全部 `values-<locale>` 登记迁移范围；没有用户或任务明确裁剪时不自设缩减默认值，项目约定与资源 skill 硬规则冲突时先核对约定的来源，无来源按源端全集执行或作为冲突上报。
5. 源 locale 缺少的键保持缺失，让平台回落 base；不按键集一致规则补写机器翻译，除非任务明确要求补译。
6. 目标限定词按源限定词的粒度映射：仅语言的 values-zh → zh/，带地区的 values-zh-rCN → zh_CN/、values-zh-rTW → zh_TW/；skill 的“最少生成 zh_CN”一类规则不用来改写源端已有的限定词；skill 正文与逐项映射表说法不一时以逐项表为准，并在映射报告写明。

## 可选检查

- 对非 base 语言目录对账：取值与 base 不同的业务字符串，都应能追溯到源端对应的 `values-<locale>` 条目。

来源支持：4 张卡 · 已知 3 次迁移（部分未记录） · 已知 3 个应用（部分未记录）

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 平台资源 android-30、android-36、android-37.0；androidfw 取 AOSP frameworks/base 的 main、android-7.0.0_r1、android-6.0.1_r81；appcompat 1.1.0、1.8.0，material 1.4.0、1.14.0，preference 1.1.1、1.2.1；build-tools 37.0.0 的 aapt2。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1、6 步〕鸿蒙资源限定词目录里，语言是 2~3 个小写字母（zh、en），文字是首字母大写加 3 个小写字母（Hans、Hant），国家或地区是 2~3 个大写字母或 3 个数字（CN、TW）；三者之间用下划线连接，区域的可选组合是 语言、语言_文字、语言_国家或地区、语言_文字_国家或地区，所以只写语言的 zh、带地区的 zh_TW、带文字的 zh_Hant 都是合法目录名；和其他限定词之间用中划线（如 zh_CN-car-ldpi）
- 〔原因 / 做法第 3、5 步〕鸿蒙应用取资源时先在和设备状态匹配的限定词目录里找；没有匹配的限定词目录、或匹配的目录里没有这个资源时，才去 base 目录找，所以限定词目录里省略的字符串键回落 base 的值；rawfile、resfile 不按设备状态匹配
- 〔原因 / 做法第 6 步〕鸿蒙限定词目录的匹配优先级是 移动国家码和移动网络码 > 区域 > 横竖屏 > 设备类型 > 颜色模式 > 屏幕密度；目录里含语言、文字限定词的，取值必须和设备状态完全一致才参与匹配（zh_CN-car-ldpi 不参与 en_US 设备的匹配）；文档这份必须一致的清单里没有国家或地区，也没写带地区的目录（如 zh_CN）对同语言、不同地区的设备是否参与匹配；设置了应用偏好语言时优先加载偏好语言对应的资源
- 〔原因〕系统语言为简体中文（zh-Hans）的设备上，鸿蒙应用 resources 里有 zh_CN 限定目录时界面取 zh_CN 的字符串；同一台设备上，只有默认 values/ 的安卓应用显示默认 values 的文案
- 〔原因 / 做法第 6 步〕安卓 7.0（API 24）起，资源目录的区域按 ResTable_config::match 判定：语言须相同（或等价）；设备区域和目录区域的文字都能确定（目录没写文字时按语言和地区推算）时要求文字相同、不看地区，推算不出时才要求目录写了的地区与设备相同。推算表里 zh 为 Hans，zh-TW、zh-HK、zh-MO（以及 zh-AU、zh-GB、zh-US 等）为 Hant，所以 values-zh 服务 zh-CN、zh-SG 等简体设备，不服务 zh-TW、zh-HK、zh-MO；values-zh-rCN 也会被 zh-SG 设备匹配，values-zh-rTW 也会被 zh-HK 设备匹配
- 〔原因 / 做法第 6 步〕安卓 6.0（API 23）的实现里，资源目录的区域匹配只看语言和地区：语言相同、目录没写地区或地区与设备相同即匹配，不看文字，所以 values-zh 服务所有中文设备（含 zh-TW、zh-HK）
- 〔例外与边界〕安卓框架字符串（@android:string/ok、cancel 等）的译文在平台资源 data/res/values-<语言>[-r<地区>]/strings.xml；中文只有 values-zh-rCN、values-zh-rTW、values-zh-rHK（另有它们的 -watch、-television 设备类型变体，不含 ok、cancel），没有仅语言的 values-zh（android-30、android-36、android-37.0 相同）。ok 在 values 为 OK、zh-rCN 为 确定、zh-rTW 与 zh-rHK 为 確定；cancel 在 values 为 Cancel、三个中文目录都是 取消
- 〔例外与边界〕androidx.preference 1.1.1、1.2.1：PreferenceThemeOverlay（1.2.1 经 BasePreferenceThemeOverlay，1.1.1 直接设）的 dialogPreferenceStyle 为 Preference.DialogPreference.Material、editTextPreferenceStyle 为 Preference.DialogPreference.EditTextPreference.Material，两者都继承 Preference.DialogPreference，其中 android:positiveButtonText=@android:string/ok、android:negativeButtonText=@android:string/cancel；偏好 XML 和 style 都没另设按钮文字时，对话框按钮显示的是框架字符串
- 〔做法第 1 步〕依赖库 aar 自带大量语言目录：appcompat 1.1.0 与 1.8.0、preference 1.1.1 与 1.2.1 各有 85 个按语言（含地区、b+ 写法）限定的 res/values-* 目录，material 1.4.0 与 1.14.0 各 81 个；三个库的中文都只有 values-zh-rCN、values-zh-rHK、values-zh-rTW
- 〔做法第 1 步〕Android SDK build-tools 37.0.0 的 aapt2 有 dump 子命令：aapt2 dump resources <apk> 打印 APK 的资源表（合并后的全部资源和各配置下的取值），aapt2 dump configurations <apk> 列出资源用到的每个配置

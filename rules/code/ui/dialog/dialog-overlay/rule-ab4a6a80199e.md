# ListPreference 没把 negativeButtonText 设为 @null 时，弹卡保留 CANCEL

审的是：代码
触发（任一种）：
- 读到：偏好 XML 里的 ListPreference / DialogPreference 没写 android:negativeButtonText="@null"；写错的样子：目标的偏好弹层（Stack 里的遮罩加卡片）一个按钮都没有，头注或报告写「无确定/取消钮」
适用范围：把 android.preference.ListPreference 的选项对话框落地成页内遮罩加卡片时的按钮和关闭路径
做法：
- 卡片底部右侧放一个负按钮：文案取取消的字符串资源，全大写显示，颜色取源端 colorAccent，14 号 FontWeight.Medium；不放确定钮
- 点选一行即写入取值并关闭；CANCEL、点遮罩、返回键三种都只关闭、不写入
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Preference.Material.DialogPreference 的 negativeButtonText = @string/cancel：XML 不写 negativeButtonText 时，负按钮文案默认就是框架的 cancel（出处：Android SDK 平台资源 data/res/values/styles_material.xml，Preference.Material.DialogPreference（按应用的 compileSdk 取对应平台））
- builder.setPositiveButton(null, null)；单选项点击后 onClick(dialog, BUTTON_POSITIVE) 再 postDismiss()：ListPreference 没有确定钮，选中即按确定处理并关闭（出处：android.preference.ListPreference#onPrepareDialogBuilder）
- TextAppearance.Material.Button：textSize = @dimen/text_size_button_material（14sp），fontFamily = sans-serif-medium，textAllCaps = true：按钮文字 14sp Medium、全大写（出处：Android SDK 平台资源 data/res/values/styles_material.xml，TextAppearance.Material.Button；values/dimens_material.xml，text_size_button_material（按应用的 compileSdk 取对应平台））
- CANCEL 为 colorAccent、14sp Medium、全大写；CANCEL、点外、返回三种取消都验证过：修好后的按钮和关闭路径（出处：卡里修好并验证过）
针对本应用要查的：
- 源端有没有改负按钮：源工程偏好 XML 里这个 ListPreference 的 android:negativeButtonText 属性；没写就是框架 cancel；写成 @null 才没有负按钮；写了别的字符串就用那条字符串
来源：1 张卡，1 个应用
- case-dadda7b6820516f5f415（Privacy Friendly 2048）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 1、诊断；取值 4 ← 诊断

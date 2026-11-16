# 设置页由 addPreferencesFromResource 挂载时，规格写进入设置页后偏好文件含默认值键

审的是：规格
触发（任一种）：
- 读到：PreferenceFragment 的 onCreate 里 addPreferencesFromResource(R.xml.x)，偏好 XML 带 android:defaultValue；写错的样子：规格只把 android:defaultValue 写成读取缺省，没写「进入设置页后偏好文件含这些键」
适用范围：规格提取时写设置页偏好默认值和偏好文件内容的契约
做法：
- 规格写明：设置页挂上时，缺持久值的偏好会把 android:defaultValue 写入偏好文件；验收写「进入设置页后偏好文件含这些键」
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Preference.dispatchSetInitialValue：偏好文件不含该 key 且有默认值时调 onSetInitialValue(false, mDefaultValue)：挂载时用默认值初始化（出处：android.preference.Preference#dispatchSetInitialValue）
- TwoStatePreference.setChecked 首次调用总会 persistBoolean：默认值随初始化被写进偏好文件（出处：android.preference.TwoStatePreference#setChecked）
针对本应用要查的：
- 哪些键有默认值、顺序如何：源工程 res/xml 下被 addPreferencesFromResource 加载的偏好 XML；按出现顺序列出每个 android:key 和 android:defaultValue
来源：1 张卡，1 个应用
- case-ad0ab84cef0e7cbc3696（Privacy Friendly 2048）：做法第 1 步 ← 建议 3

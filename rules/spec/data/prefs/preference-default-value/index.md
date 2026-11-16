# 偏好 XML 的 android:defaultValue

agent 会看到什么：读到 PreferenceFragment 的 onCreate 里 addPreferencesFromResource(R.xml.x)，偏好 XML 带 android:defaultValue；规格只把它写成读取缺省，没写进入设置页后偏好文件含这些键

## 规矩

- rule-dc5fd87c4bb6｜设置页由 addPreferencesFromResource 挂载时，规格写进入设置页后偏好文件含默认值键｜读到：PreferenceFragment 的 onCreate 里 addPreferencesFromResource(R.xml.x)，偏好 XML 带 android:defaultValue；写错：规格只把 android:defaultValue 写成读取缺省，没写「进入设置页后偏好文件含这些键」

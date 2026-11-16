# 设置页与偏好存储

读到 addPreferencesFromResource 加载的偏好 XML（Preference、SwitchPreference、ListPreference、EditTextPreference）、SharedPreferences / DataStore 的键和默认值、偏好标记控制的一次性引导，规格里写设置页、偏好表和首次进入行为时

## 触发族

- [偏好 XML 里平台偏好项的默认外观和对话框](preference-default-look/index.md)（8 条）：读到 addPreferencesFromResource 加载的偏好 XML（PreferenceActivity / PreferenceFragment 或 AndroidX Preference），Preference、SwitchPreference、ListPreference、EditTextPreference 没写 widgetLayout、dialogLayout、style，源码里没有布局和对话框代码；规格写「开关行等价」「Select / bindSheet」「自定义输入弹窗」「行尾箭头」「双按钮 OK/Cancel」或「精确样式值待核」
- [偏好 XML 的 android:defaultValue](preference-default-value/index.md)（1 条）：读到 PreferenceFragment 的 onCreate 里 addPreferencesFromResource(R.xml.x)，偏好 XML 带 android:defaultValue；规格只把它写成读取缺省，没写进入设置页后偏好文件含这些键
- [SharedPreferences / DataStore 的偏好键和默认值](prefs-keys-defaults/index.md)（6 条）：读到 DataStore getter 写成 preferences[KEY] == true 或带 ?: 默认值、Compose 里对 collectAsState 收集的状态判 == null、键表里同类数据分成几组独立键、全局键值工具要先 init(context)；规格的偏好表、触发条件、AC 写成三态 null、「首次进入」、合并的两组持久化或只写「已实现」
- [偏好标记控制的一次性引导](pref-flag-onetime-guide/index.md)（1 条）：读到源码里引导图只在某个偏好标记为真时 VISIBLE、点击隐藏，显示后随即调 setter 写回标记，布局里引导 ImageView 为 match_parent 加 android:scaleType="fitXY"；行为笔记或规格里没有这个首次引导项
- [onPreferenceChange 回调里的联动流程](preference-change-flow/index.md)（1 条）：读到源码 onPreferenceChange 返回 true（新值立即生效）、随后才弹验密这类确认弹窗、成功再设同值；验收条目写成「确认成功才真正切换、失败后开关回弹」，和源码顺序相反，没写每一步的落值时刻和失败分支

# 设置页与偏好项

源端有 PreferenceFragment / PreferenceActivity、res/xml 里的 Preference、ListPreference、SwitchPreference，目标端有 List / ListItem 写的设置行时

## 触发族

- [平台主题下 ListView 和偏好界面的默认外观](platform-list-preference-look/index.md)（8 条）：读到 ListView、GridView、ExpandableListView、PreferenceActivity 没写 divider、listSelector、scrollbars 等，外观来自 Theme.Holo 等平台主题；交回的 List 缺分隔线或末行那条、按压态用 opacity 或自拟色、偏好行和对话框的几何凭记忆写，或 CheckBoxPreference 写成 Toggle
- [框架 PreferenceFragment 的设置页](framework-preference/index.md)（5 条）：读到源端 android.preference.PreferenceFragment 用 addPreferencesFromResource 加载偏好 XML（SwitchPreference、ListPreference、android:defaultValue）；产物里 List / ListItem 写的设置行、行内开关和 preferences 读写
- [带 android:icon 的 Preference 行](preference-icon-row/index.md)（1 条）：读到 res/xml 里 <Preference android:icon="@drawable/…">，没有任何箭头元素，派工或转换表却写「箭头行」；产物里行尾加了 Text('›') 或 chevron 箭头 Image，图标按 24vp 画

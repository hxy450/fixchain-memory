# Manifest 属性依赖缺省时，到平台 attrs_manifest.xml 查缺省语义，写成目标配置的显式值

审的是：规格
触发（任一种）：
- 读到：AndroidManifest 的 <application> / <activity> 没写 android:allowBackup、android:screenOrientation、android:windowSoftInputMode 一类属性，依赖平台缺省；写错的样子：规格只写「按系统缺省」「unspecified」或只列权限，没有缺省的出处和目标配置值
适用范围：规格阶段把 AndroidManifest 的属性落到 module.json5、备份配置和窗口配置时
做法：
- 按属性名到平台资源 attrs_manifest.xml（windowSoftInputMode 在 attrs.xml）找 <attr> 和注释，读出缺省值和枚举含义；缺省随条件而变的（如 adjustUnspecified 看有没有可滚动视图），回源布局核条件
- 查目标端对应配置项自己的缺省（module.json5 abilities 的 orientation、backup_config.json 的 allowToBackupRestore、setKeyboardAvoidMode），两端缺省不同的写成显式值，每项指派实现
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- android:allowBackup 默认 true：例：源端没写时允许备份（出处：Android SDK 平台资源 data/res/values/attrs_manifest.xml，allowBackup（按应用的 compileSdk 取对应平台））
- allowToBackupRestore 默认 false：例：目标端不写就不允许备份，和源端缺省相反，要显式写（出处：app-file-backup-extension.md，allowToBackupRestore）
- adjustUnspecified：the system will automatically select between resize and pan modes, depending on whether the content of the window has any layout views that can scroll their contents：例：缺省随条件而变的属性，要回源布局核有没有可滚动视图（出处：Android SDK 平台资源 data/res/values/attrs.xml，windowSoftInputMode 的 adjustUnspecified（按应用的 compileSdk 取对应平台））
针对本应用要查的：
- 源端这个属性的实际取值：源 AndroidManifest 里该 <activity> 和 <application> 的属性；没写时看它引用的主题里有没有同名的窗口属性（如 android:windowSoftInputMode）；写了就按值查含义；都没写就按平台缺省写，并注明缺省的出处
未核实：未声明 screenOrientation 时目标写 unspecified（或不写）还是 auto_rotation_restricted，族里两条规矩的说法不同
来源：2 张卡，2 个应用
- case-1b03af761b99c891e236（Blockinger）：做法第 1 步 ← 建议 1
- case-cc22f6cc1041c8cc1129（MifareClassicTool）：做法第 1 步 ← 建议 4；做法第 2 步 ← 建议 4

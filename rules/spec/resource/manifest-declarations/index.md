# Manifest 里 application 和 activity 的声明

agent 会看到什么：读过的 AndroidManifest 里 <application> / <activity> 的 allowBackup、screenOrientation、windowSoftInputMode、android:label、usesCleartextTraffic，或这些没写、依赖平台缺省；交回的规格没写它们的缺省语义、目标配置值和对应验收

## 通用查法

### Manifest 属性依赖缺省时，到平台 attrs_manifest.xml 查缺省语义，写成目标配置的显式值

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

## 规矩

- rule-5e35432f6b1a｜规格逐项列出 manifest 的 application/activity 属性和缺省语义，映射到目标配置｜读到：AndroidManifest 的 <application android:allowBackup="false">，<activity> 没写 android:screenOrientation、android:windowSoftInputMode（依赖平台缺省）；写错：规格或功能基线的配置段只写权限（或「requestPermissions 为空」），没有备份、屏幕方向、软键盘避让的映射；界面图里方向记为 unspecified、软键盘记为 unknown 却没给目标值，也没有对应的实现任务
- rule-187734312cc1｜源 activity 声明 screenOrientation 时，规格写进页方向验收条目，不只写全屏｜读到：AndroidManifest.xml 的 <activity> 声明 android:screenOrientation="sensorLandscape" 等方向值；onCreate 里另有 FLAG_FULLSCREEN；写错：页面或功能规格只有「FLAG_FULLSCREEN 全屏」一条，没有屏幕方向的验收条目
- rule-2d350a0359e8｜决策写横竖屏双布局时，把 EntryAbility 的 orientation 列为 module.json5 必做项｜读到：源 `AndroidManifest.xml` 的 activity 没有 `android:screenOrientation`；源有 `layout-land` / `values-land` 或「两个方向都可用」类文案；写错：规格或决策台账只写「横竖屏双布局全支持」「无 screenOrientation（双方向）」这类安卓语义，技术必做项和 feature-base 的 module.json5 节只列 requestPermissions，没有 ability orientation 条目
- rule-e31fce120fd6｜未声明 windowSoftInputMode 且含 EditText 时，验收写首屏焦点分支和键盘避让模式｜读到：manifest 里该 activity 没有 android:windowSoftInputMode；EditText 前面只有可能为空的 ListView 或没有常驻可获焦视图；源码没有 requestFocus / showSoftInput；写错：规格只在 Manifest 事实行写“无 windowSoftInputMode（默认弹出）”；验收里没有首屏谁获焦、是否自动弹键盘，也没指派实现
- rule-207eda42aab8｜给 android:label 写验收条目时只写键名或照抄 strings.xml 的值，不补未读到的字面值｜读到：源 Manifest 的 android:label="@string/app_name"，只给出资源键名，值要到 res/values*/strings.xml 查；写错：验收条目写成「app=@string/app_name（"某个名字"）」，括号里的字面值没有出处、和 strings.xml 不符；真值锚点指向 Manifest，没有决策锚点
- rule-d811397a16e0｜台账给日志上传定 HTTPS 或只传快照时，逐项写明与安卓明文策略和打包清单的差异｜读到：安卓 AndroidManifest 的 <application> 写了 android:usesCleartextTraffic="true"（或 android:networkSecurityConfig）；上传函数先向服务端取预签名地址再 PUT，ZIP 里有日志目录全部留存文件、设备信息和 ObjectBox 各表导出；写错：决策台账或规格把上传定成「经 presign → HTTPS PUT」「只传快照、不上传完整数据库」这类收窄约束，却没写安卓清单的明文策略和上传函数的实际打包清单，也没把差异逐项标成待用户确认
- rule-495e3ca88c5e｜Activity 未锁方向且自处理旋转时，规格写明 Ability 的 orientation 和 launchType｜读到：AndroidManifest.xml 的 <activity> 没有 android:screenOrientation（缺省可旋转），android:configChanges 含 orientation，另有 android:launchMode（如 singleTop）；写错：决策台账和 module.json5 映射节里没有方向、configChanges、launchMode 的决策项；「设备形态」一项只答手机或平板，没给 EntryAbility 的 orientation、launchType，也没写旋转时页面是否重建
- rule-db404fd12347｜承载 module.json5 声明的功能规格，把屏幕方向与权限并列写成验收条目｜读到：页面规格的「Manifest 解析」行或参考规格的平台目标值表写着「未声明 screenOrientation → module.json5 EntryAbility orientation: auto_rotation_restricted」，而页面规格的输出文件不含 module.json5；写错：功能规格里 module.json5 相关的验收条目只有权限声明和备份声明，没有 orientation 条目，或写成「页面规格已定、引用不重写」；有的还把旋转列为 onConfigurationUpdate 要重放的配置变化，却没有让窗口随传感器旋转的条目

# Activity 未锁方向且自处理旋转时，规格写明 Ability 的 orientation 和 launchType

审的是：规格
触发（任一种）：
- 读到：AndroidManifest.xml 的 <activity> 没有 android:screenOrientation（缺省可旋转），android:configChanges 含 orientation，另有 android:launchMode（如 singleTop）；写错的样子：决策台账和 module.json5 映射节里没有方向、configChanges、launchMode 的决策项；「设备形态」一项只答手机或平板，没给 EntryAbility 的 orientation、launchType，也没写旋转时页面是否重建
适用范围：规格提取和计划阶段，为 Manifest 里 Activity 的方向、配置变化和启动模式属性确定目标端归属时
做法：
- 逐个 Activity 提取并回答 screenOrientation（缺省 = 可旋转）、configChanges 是否含 orientation、launchMode，写进 module.json5 映射节：给出对应 UIAbility 的 "orientation"（如 auto_rotation_unspecified）、"launchType"，以及旋转不重建的实现契约
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- screenOrientation 缺省 unspecified：No preference specified: let the system decide the best orientation：源端没写时随传感器和用户设置旋转（出处：Android SDK 平台资源 data/res/values/attrs_manifest.xml，screenOrientation 的 unspecified（按应用的 compileSdk 取对应平台））
- configChanges 的 orientation 标志：The screen orientation has changed, that is the user has rotated the device：Activity 自己处理旋转，不随旋转重建（出处：Android SDK 平台资源 data/res/values/attrs_manifest.xml，configChanges 的 orientation（按应用的 compileSdk 取对应平台））
- orientation 缺省 unspecified（由系统自动判断显示方向）；auto_rotation_unspecified：受开关控制和由系统判定的自动旋转模式：目标端不写就不会跟着源端可旋转（出处：module-configuration-file.md，abilities 标签的 orientation）
- launchType 取 multiton、singleton、specified（standard 是 multiton 的曾用名），缺省 singleton：launchMode 要映射到的目标端字段（出处：module-configuration-file.md，abilities 标签的 launchType）
- 给 EntryAbility 加 "orientation": "auto_rotation_unspecified" 后横屏可达：可旋转的源 Activity 对应的写法（出处：卡里修好并验证过）
未核实：卡里上机所用 SDK 是 API 24（6.1.1），按本机文档和 API 23 声明核实
来源：1 张卡，1 个应用
- case-69a2766b2050118ebd5a（omni-notes-hmos）：做法第 1 步 ← 建议 1；取值 5 ← 诊断

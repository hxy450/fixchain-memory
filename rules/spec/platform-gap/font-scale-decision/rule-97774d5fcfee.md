# 裁定大字体时不以有无显式 fontScale 代码为准，源端有随系统字号缩放的文本就判为迁移

审的是：规格
触发（任一种）：
- 读到：源端主体是固定 px 字号的 Canvas 自绘，但仍用 AlertDialog.Builder(...) 的系统对话框、Toast、菜单或 sp 单位的文本；Manifest 的 Activity 没有声明 android:configChanges="fontScale"；写错的样子：决策台账写「大字体 | 不适用（Canvas 固定字号，Android 端无 fontScale 适配）」，没列系统对话框等随系统字号缩放的文本，也没写目标落点
适用范围：横切能力裁定里的大字体（系统字号缩放）一项
做法：
- 逐项列出源端随系统字号缩放的文本来源（系统 AlertDialog / Toast / 菜单、sp 单位文本），并看 Manifest configChanges 是否含 fontScale：不含时字号变化由系统重建 Activity；只有全部文本都是固定 px 自绘才判不适用
- 有任一这类文本就判为迁移，决策里写出目标落点：AppScope/app.json5 加 "configuration": "$profile:configuration"，profile 里 fontSizeScale = followSystem、fontSizeMaxScale 按源端系统字号上限取；固定 px 的 Canvas 部分不变
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- fontScale：value="0x40000000"，用户选了新的全局字号：configChanges 的取值；没声明时字号变化由系统重建 Activity（出处：Android SDK 平台资源 data/res/values/attrs_manifest.xml，configChanges 的 fontScale（按应用的 compileSdk 取对应平台））
- COMPLEX_UNIT_SP = 2：Value is a scaled pixel：sp 是随系统字号缩放的单位（出处：android.util.TypedValue#COMPLEX_UNIT_SP）
- fontSizeScale 缺省值为 nonFollowSystem：目标默认不跟随系统字号，要显式配置（出处：app-configuration-file.md，configuration标签）
来源：1 张卡，1 个应用
- case-a824609ada4969e6d96c（2048）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 2

# 偏好 XML 里平台偏好项的默认外观和对话框

agent 会看到什么：读到 addPreferencesFromResource 加载的偏好 XML（PreferenceActivity / PreferenceFragment 或 AndroidX Preference），Preference、SwitchPreference、ListPreference、EditTextPreference 没写 widgetLayout、dialogLayout、style，源码里没有布局和对话框代码；规格写「开关行等价」「Select / bindSheet」「自定义输入弹窗」「行尾箭头」「双按钮 OK/Cancel」或「精确样式值待核」

## 通用查法

### 偏好项没写布局和样式时，规格按平台或 AndroidX 偏好资源写出行和对话框的可见契约

审的是：规格
触发（任一种）：
- 读到：偏好 XML 里的 Preference、SwitchPreference、ListPreference、EditTextPreference 没写 android:widgetLayout、dialogLayout、style，源码里没有布局和对话框代码；写错的样子：规格写「开关行等价」「Select / bindSheet」「行尾箭头」「值待核」，没有行几何、行尾控件、对话框外观和按钮
适用范围：偏好项转成 ArkUI 设置页时，规格里行和对话框的转换决策
做法：
- 按所在的库找资源：android.preference 到 SDK 平台资源的 preference_*、select_dialog_* 布局和 Preference.* 样式；AndroidX 到 androidx.preference 包内 res/layout 和 values.xml
- 从默认样式读出行布局、widgetLayout 和对话框按钮，顺着 ?attr/、@dimen/ 读到值；行尾和按钮只按源 XML 和样式写
- 规格写成可见契约；查过仍缺的才标待核并写检索路径
针对本应用要查的：
- 偏好项用的是哪个库、哪一版资源：源码里设置页继承的类（android.preference.PreferenceActivity / PreferenceFragment，或 androidx.preference 的类），模块构建脚本的 compileSdk 和 androidx.preference 依赖版本；android.preference 取对应平台的 data/res，AndroidX 取对应版本的包；应用主题 parent 是 Theme.Holo 用 *_holo_dark，Theme.Holo.Light 用 *_holo_light
- 应用主题有没有改偏好行和对话框的外观：源工程 res/values 下的 styles / themes XML，按应用主题的 parent 和 alertDialogTheme、backgroundDimAmount、dialogCornerRadius、colorAccent 这几个 item 找；有覆写的取覆写值，没有的取库默认；例：android-36 平台下 Theme.Material 的 backgroundDimAmount 是 0.6
未核实：AndroidX Preference 弹出的对话框外观，本族规矩没有查过对应的库资源
来源：3 张卡，3 个应用
- case-85baa9234cc4f4798784（AntennaPod）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3
- case-a8bb009f2c5e1b854f32（Blockinger）：做法第 1 步 ← 建议 1；做法第 3 步 ← 建议 1
- case-dadda7b6820516f5f415（Privacy Friendly 2048）：做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 1

## 规矩

- rule-04bb49c30a71｜PreferenceActivity 配 Theme.Holo 时，规格先查平台偏好布局和样式写出几何，查过仍无才标待核｜读到：Activity 继承 android.preference.PreferenceActivity，应用主题 parent 是 android:Theme.Holo*，页面没有布局 XML，只有 res/xml 偏好项（CheckBoxPreference、PreferenceCategory、带 android:icon 的 Preference）；写错：规格写「Holo 小字分类头样式——精确样式值待核」「值取不到处标待核」，没写列表内边距、行高、分隔线规则和按压色，也没写检索过哪里
- rule-8a482ea1759a｜AndroidX Preference 没有 widgetLayout 时，规格里的行组成不写行尾箭头｜读到：偏好 XML 里 <Preference> 节点只有 key、title、summary、icon，没有 android:widgetLayout 或 app:widgetLayout；写错：规格的行组成或转换决策写「Preference 行 + 箭头」「chevron_right」「右箭头 SymbolGlyph」，理由是「Material 列表行样式」这类源端没有的依据
- rule-e5156a855e04｜SwitchPreference 只靠平台默认外观时，规格写开关可见契约，不写「Toggle 等价」｜读到：PreferenceFragment / addPreferencesFromResource 加载的 SwitchPreference（或 Switch、CheckBoxPreference）没写 android:widgetLayout、style、android:thumb、android:track；写错：转换决策写成「SwitchPreference | Toggle({ type: ToggleType.Switch }) | 开关行等价」，没写轨道和拇指尺寸、两态颜色、拇指投影、切换动画、点击归属
- rule-258c89191971｜DialogPreference 的对话框，规格写平台 AlertDialog 可见契约，不写 Select 或自绘弹窗｜读到：偏好 XML 里有 ListPreference 等 DialogPreference，由 PreferenceFragment 的 addPreferencesFromResource 加载，没设 dialogLayout；源码里看不到 AlertDialog.Builder；写错：转换决策写成「Select 组件或 bindSheet 选项单」，没有遮罩、卡宽、圆角、标题、单选行、按钮和取消路径
- rule-ed1381976d84｜ListPreference 对话框只留 Cancel，按钮集合按框架默认推导｜读到：<ListPreference> 没写 android:negativeButtonText；<EditTextPreference> 写了或没写 positiveButtonText / negativeButtonText；写错：规格给 ListPreference 写「双按钮 OK/Cancel」或「无按钮」，或照别的对话框类推按钮集合
- rule-2d31a38c8382｜ListPreference、EditTextPreference 的弹窗，规格写居中对话框不写 bindSheet｜读到：源端 ListPreference、EditTextPreference（由 preference / preference-ktx 库运行时构建，项目里没有对应布局 XML），或 MaterialDialog 的单选列表；写错：规格的转换决策表写成「→ bindSheet 弹层」「bindSheet + TextInput 表单弹层」「bindSheet 单选列表」
- rule-9a3232ef35df｜三方 UI 组件在本仓没有源码时，规格只写调用点可见的结构，不写未核实的装饰｜读到：ProvidePreferenceTheme 里直接排列 Preference(title, icon, onClick)，调用点没有 divider，也没有尾部图标；库（me.zhanghai.compose.preference）在本仓没有源码；写错：规格写「Preference 自带分隔线/内边距主题」，转换决策给每行加 chevron_right，或给出行高等未查实的近似几何值

# 没写样式、外观由平台主题提供的控件

agent 会看到什么：源布局的 <SeekBar>、<ListView> 等没写 style、divider、thumb，或 ActionBar 不在布局里，Activity 主题的 parent 链止于 android:Theme.Holo 等平台主题，规格只写「直接映射」「List + ForEach」「标题栏 + 返回箭头」

## 通用查法

### 源控件没写样式、外观由平台主题提供时，规格顺主题链查出实际取值，写成转换决策行

审的是：规格
触发（任一种）：
- 读到：源布局的 <SeekBar>、<ListView> 等平台控件没写 style、divider、thumb 这类外观属性，或 ActionBar 由主题提供；Activity 主题的 parent 链止于 android:Theme.Holo 等平台主题；写错的样子：规格的转换决策只写「SeekBar → Slider 直接映射」「List + ForEach」「标题栏 + 返回箭头」，没写外观提供方和从平台资源读到的颜色、尺寸、图片
适用范围：规格提取阶段，页面里有外观由平台主题隐式提供的控件时
做法：
- 从 Manifest 的 android:theme 顺 parent 链找到平台主题，在它的 themes_*.xml 里按控件找样式项（seekBarStyle、listDivider、actionBarStyle 等），定外观提供方
- 到 styles_*.xml 读这个样式的各 item，顺着 ?attr/、@drawable/、@dimen/ 读到颜色、dp 和图片，限定词目录的差异一并读
- 转换决策表给这个控件单列一行：外观提供方、读到的取值、触摸或绘制规则；用到的颜色列进要新增的资源
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Widget.Holo.ListView：divider = ?attr/listDivider；Theme.Holo：listDivider = @drawable/list_divider_holo_dark：例：Theme.Holo 下没写 divider 的 ListView，顺 ?attr 读到主题的分隔线图（出处：Android SDK 平台资源 data/res/values/styles_holo.xml，Widget.Holo.ListView；data/res/values/themes_holo.xml，listDivider（按应用的 compileSdk 取对应平台））
- Theme.Holo 的 actionBarStyle = @style/Widget.Holo.ActionBar，actionBarSize = @dimen/action_bar_default_height（values 48dip、values-land 40dip）：例：主题项指向样式和尺寸资源，尺寸随限定词目录变（出处：Android SDK 平台资源 data/res/values/themes_holo.xml，Theme.Holo；data/res/values*/dimens.xml，action_bar_default_height（按应用的 compileSdk 取对应平台））
针对本应用要查的：
- 控件的外观提供方：源工程 AndroidManifest.xml 的 android:theme（Activity 或 application）和 res/values*/styles.xml 的 parent 链，到对应平台 data/res/values/themes_*.xml 里找这个控件的样式项；读出样式名，到 styles_*.xml 取各 item
- 样式里引用的颜色、尺寸和图片：对应平台 data/res/values*/dimens.xml 等资源文件和 data/res/drawable-<密度>/ 下的同名图；?attr/ 回到主题取值，@dimen/ 按限定词目录各读一遍；9-patch 图读像素颜色和高度，px 除以密度系数得 dp
未核实：主题 parent 链里同名项的覆盖先后，族里规矩只按「顺 parent 找到平台主题」用过，没有单独查证
来源：3 张卡，1 个应用
- case-5f607109511beae4aec1（Blockinger）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1
- case-c3ff122a5abfda1fa55d（Blockinger）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 1
- case-f7cfc36e8dc61295fe43（Blockinger）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3；做法第 3 步 ← 建议 3

## 规矩

- rule-896043257bea｜源端用 Theme.Holo 且带 ActionBar 时，规格每页写一条 ActionBar 外观决策行｜读到：styles.xml 的主题 parent 链止于 android:Theme.Holo（未用 NoActionBar / FEATURE_NO_TITLE、未自定义 actionBarStyle）；代码有 setDisplayHomeAsUpEnabled(true)；菜单项 android:showAsAction="ifRoom|withText"；manifest 有 android:icon；写错：规格只写「标题栏 + 返回箭头 → pop」或「图标+文字」，没有背景 drawable、应用图标、标题字号、Up 与溢出图标、values-land / values-w480dp 差异，也没登记为多页共享组件
- rule-dc0f4fb30809｜页面规格给每个未写样式的平台控件单列转换决策行：外观提供方、SDK 取值、触摸规则｜读到：源布局 <SeekBar> 没写 style、thumb、progressDrawable；映射参考写「SeekBar → Slider 直接映射」，外观属性表却写 android:thumb、thumbOffset「无直接对应，需自定义实现」；写错：转换决策表里没有这个控件的外观或触摸取值行，状态表只写「…的 Slider(0..N)」
- rule-fd43492cb850｜ListView 没声明 divider 时，规格按实际主题写出 listDivider 的颜色、高度和末行｜读到：<ListView>（或 ListActivity 的 @android:id/list）没写 android:divider、android:dividerHeight，Activity 主题继承 Theme.Holo / Theme.Material 等框架主题，分隔线由主题 listDivider 隐式提供；写错：规格的列表转换决策只写「List + ForEach，简单两行列表」或 List + ListItem、edgeEffect、滚动条、按压态，没有主题分隔线的颜色、高度、是否含末行；或者写成由 List.divider 承担分隔线
- rule-84d5572ff53a｜生效主题提供窗口级外观时，规格逐项写出状态栏色、窗口底色、标题栏投影并指派承接者｜读到：生效主题是 Material 系（如 Theme.Material.Light.DarkActionBar），布局 XML 里没有窗口背景、状态栏色和标题栏投影，窗口用框架 ActionBar；写错：全局约定或页面规格写「仅做系统栏默认避让」「系统栏默认」，没有状态栏底色与图标深浅、窗口底色、ActionBar 背景/标题色/投影的条目，也没写由谁承接
- rule-b4b29820aba1｜规格给框架主题的勾选框写转换决策时，形态约束和外观来源分开写，组件栏不直接写 Checkbox｜读到：源端 CheckBoxPreference / CheckBox 的勾选图由框架主题提供（平台 drawable btn_checkbox_checked_mtrl / btn_checkbox_unchecked_mtrl）；写错：转换表写「CheckBoxPreference | Checkbox（勾选框，非 Switch/Toggle）」，只写了形态，没写外观来源；实现者把它读成指定 ArkUI Checkbox 组件

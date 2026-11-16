# 源控件没写样式、外观由平台主题提供时，规格顺主题链查出实际取值，写成转换决策行

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

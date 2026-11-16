# 页面规格给每个未写样式的平台控件单列转换决策行：外观提供方、SDK 取值、触摸规则

审的是：规格
触发（任一种）：
- 读到：源布局 <SeekBar> 没写 style、thumb、progressDrawable；映射参考写「SeekBar → Slider 直接映射」，外观属性表却写 android:thumb、thumbOffset「无直接对应，需自定义实现」；写错的样子：转换决策表里没有这个控件的外观或触摸取值行，状态表只写「…的 Slider(0..N)」
适用范围：规格提取时页面里有外观由框架主题隐式提供的平台控件（对话框内容视图里的也算）
做法：
- 转换决策表给这类控件单列一行：外观提供方（如 Widget.Holo.SeekBar）、从 SDK 平台资源取到的尺寸、颜色和图片名、触摸取值规则
- 映射参考的「直接映射」只覆盖值域和回调；外观表里标「无直接对应」的 thumb、thumbOffset 由主题隐式提供时，同样写进这一行
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Widget.Holo.SeekBar：thumb @drawable/scrubber_control_selector_holo，thumbOffset 16dip，paddingStart / paddingEnd 16dip，progressDrawable @drawable/scrubber_progress_horizontal_holo_dark：决策行里外观提供方和要写的几项（出处：Android SDK 平台资源 data/res/values/styles_holo.xml，Widget.Holo.SeekBar（按应用的 compileSdk 取对应平台））
针对本应用要查的：
- 控件的外观提供方：源工程 AndroidManifest.xml 的 android:theme 和 styles.xml 的 parent 链，到对应平台的 themes_*.xml 里找 seekBarStyle、progressBarStyle 等；读出样式名后到 styles_*.xml 取各 item，图片按名字到 drawable* 目录找
来源：1 张卡，1 个应用
- case-f7cfc36e8dc61295fe43（Blockinger）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3

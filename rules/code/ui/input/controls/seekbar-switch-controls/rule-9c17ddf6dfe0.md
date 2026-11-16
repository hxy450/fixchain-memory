# 源控件没写样式时，按主题父链到 SDK 平台资源读控件外观，写成显式的尺寸、图和颜色

审的是：代码
触发（任一种）：
- 读到：布局里 <SeekBar>、Switch 等平台控件没写 style、android:thumb、android:track、android:progressDrawable，外观来自 android:Theme.*；写错的样子：目标用 Slider、Toggle 默认外观，只改 trackColor / blockColor 近似色，或标「待核色值」
适用范围：源控件外观由框架主题的控件样式提供时
做法：
- 从 AndroidManifest.xml 的 android:theme 顺 styles.xml 的 parent 链找到 android:Theme.* 那层，在 Android SDK 平台资源 themes_*.xml 读控件样式属性（如 seekBarStyle → Widget.Holo.SeekBar）
- 到 styles_*.xml 读这个样式的高度、内边距、thumbOffset，顺 progressDrawable、thumb 或 drawable/、color/ 下的 selector 读出图源和两态颜色；?attr/ 颜色回主题再解
- 按读出的值写：位图复制进 media；几何、颜色和默认组件对不上时写自定义组件，不用默认外观改色了事
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Theme.Holo 的 seekBarStyle = @style/Widget.Holo.SeekBar：例：Holo 主题下 SeekBar 外观的提供方（出处：Android SDK 平台资源 data/res/values/themes_holo.xml，seekBarStyle（按应用的 compileSdk 取对应平台））
- 轨道颜色：state_checked → ?attr/colorControlActivated；其余 → ?attr/colorForeground：例：框架开关轨道的两态颜色取主题属性（出处：Android SDK 平台资源 data/res/color/switch_track_material.xml（按应用的 compileSdk 取对应平台））
针对本应用要查的：
- 源控件实际用的框架主题和控件样式：源工程 AndroidManifest.xml 的 android:theme、res/values*/styles.xml 的 parent 链、祖先布局的 android:theme；再到 Android SDK 平台资源（按 compileSdk 取对应平台）的 themes_*.xml；找到 android:Theme.* 那层，读控件样式属性指向的样式名
- 样式里的尺寸、图源和两态颜色：同一平台 data/res/values/styles_*.xml，以及 drawable/、color/ 下被引用的 xml 和各密度图片；顺 @drawable/、@color/ 读到 layer-list、selector 的各项；?attr/ 颜色回应用主题解，没写的落到平台 themes_*.xml。例：Theme.Material.Light 下 colorSwitchThumbNormal 是 switch_thumb_material_light，正常态 #fff1f1f1
未核实：除 SeekBar 的 seekBarStyle 外，Switch、ProgressBar、RatingBar 等控件在平台主题里的样式属性名，族里规矩没有查实
来源：2 张卡，2 个应用
- case-01ea7d8b923cd659dbba（Privacy Friendly 2048）：做法第 2 步 ← 建议 3；做法第 3 步 ← 建议 3
- case-f7cfc36e8dc61295fe43（Blockinger）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；做法第 3 步 ← 诊断

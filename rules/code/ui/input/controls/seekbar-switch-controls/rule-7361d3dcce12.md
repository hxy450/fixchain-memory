# 未写样式的平台 SeekBar 先按主题到 SDK 平台资源取外观，位图拇指和双粗细轨道用自定义组件

审的是：代码
触发（任一种）：
- 读到：布局里 <SeekBar>（或 ProgressBar、RatingBar）没写 style、android:thumb、android:progressDrawable，应用主题父链是 android:Theme.Holo 等框架主题；写错的样子：目标写成 Slider({ min, max, step, style: SliderStyle.OutSet }) 只配 trackColor / selectedColor / blockColor 近似色，报告标「待核色值」
适用范围：源控件外观由框架主题的控件样式提供（主题父链是 android:Theme.*）时
做法：
- 按主题找提供外观的框架样式：主题的 seekBarStyle → Widget.Holo.SeekBar；在 SDK 平台资源读它的高度、thumbOffset、paddingStart/End，再顺着 progressDrawable、thumb 到 drawable 里取轨道、进度和拇指的图
- 轨道和进度粗细不同、拇指是位图时，把平台的拇指 PNG（normal、pressed）复制进目标 media，写自定义组件：左右内边距、轨道和进度各自的粗细与颜色、拇指用图片、拖动时换 pressed 图；不用 Slider 改色后标「待核」
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Theme.Holo 的 seekBarStyle = @style/Widget.Holo.SeekBar（Light 主题是 Widget.Holo.Light.SeekBar）：Holo 主题下 SeekBar 外观的提供方（出处：Android SDK 平台资源 data/res/values/themes_holo.xml，seekBarStyle（按应用的 compileSdk 取对应平台））
- Widget.Holo.SeekBar：progressDrawable @drawable/scrubber_progress_horizontal_holo_dark，minHeight / maxHeight 13dip，thumb @drawable/scrubber_control_selector_holo，thumbOffset 16dip，paddingStart / paddingEnd 16dip：外观的尺寸和图源（出处：Android SDK 平台资源 data/res/values/styles_holo.xml，Widget.Holo.SeekBar（按应用的 compileSdk 取对应平台））
- scrubber_progress_horizontal_holo_dark 是 layer-list：background scrubber_track_holo_dark，secondaryProgress scrubber_secondary_holo，progress scrubber_primary_holo（各密度的 .9.png）：轨道和进度是两张不同的九宫图，粗细不同（出处：Android SDK 平台资源 data/res/drawable/scrubber_progress_horizontal_holo_dark.xml）
- scrubber_control_selector_holo：按下 scrubber_control_pressed_holo，默认 scrubber_control_normal_holo（各密度 PNG）：拇指是位图，按下换图（出处：Android SDK 平台资源 data/res/drawable/scrubber_control_selector_holo.xml）
- 左右内边距 16；轨道 #80666666、0.76vp，进度 #33B5E5、3.05vp；拇指用平台 PNG，拖动时换 pressed 图：返修后对照平台资源复刻的 Holo SeekBar（dark 主题）（出处：卡里修好并验证过）
针对本应用要查的：
- 源控件实际用的框架主题：源工程 AndroidManifest.xml 的 android:theme，和 res/values*/styles.xml 里这个主题的 parent 链；祖先布局的 android:theme 覆盖；一直找到 android:Theme.* 那一层，再到对应平台的 themes_*.xml 读 seekBarStyle 等控件样式名
来源：1 张卡，1 个应用
- case-f7cfc36e8dc61295fe43（Blockinger）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断；取值 5 ← 诊断

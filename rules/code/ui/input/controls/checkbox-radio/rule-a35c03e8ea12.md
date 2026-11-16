# 框架单选对话框的行按 Material 样式自绘圆环、行高 48，不用鸿蒙 Radio 默认样式

审的是：代码
触发（任一种）：
- 读到：源端单选列表来自框架 select_dialog_singlechoice_material（ListPreference 的 setSingleChoiceItems），圆环是 ?attr/listChoiceIndicatorSingle（btn_radio_material_anim）；写错的样子：目标单选行用 Radio({ group, value }) 加 .radioStyle(...)，行高、字号按估值（行上下 14、16 号）
适用范围：把框架 AlertDialog 的单选列表（ListPreference 等）落地成页内弹卡里的选项行时
做法：
- 每行自绘：最小高 48，左内边距 20，圆环和文字间距 20，文字 18 号；圆环外径 20、环宽 2，选中时中心实心点直径 10
- 选中的环和点用源端 colorAccent，未选的环用源端未选色，不用 Radio 的默认配色
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- CheckedTextView：minHeight = ?attr/listPreferredItemHeightSmall，paddingStart = @dimen/select_dialog_padding_start_material，drawablePadding = @dimen/select_dialog_drawable_padding_start_material，textAppearance = ?attr/textAppearanceMedium：单选行的结构（出处：Android SDK 平台资源 data/res/layout/select_dialog_singlechoice_material.xml（按应用的 compileSdk 取对应平台））
- listPreferredItemHeightSmall = 48dip；select_dialog_padding_start_material = 20dp；select_dialog_drawable_padding_start_material = 20dp；text_size_medium_material = 18sp：行高 48、左内边距 20、圆环到文字 20、文字 18sp（出处：Android SDK 平台资源 data/res/values/themes_material.xml，listPreferredItemHeightSmall；values/dimens_material.xml，select_dialog_padding_start_material、text_size_medium_material（按应用的 compileSdk 取对应平台））
- btn_radio_on_mtrl：32dp 画布，外环半径 9、strokeWidth 2，中心点半径 5，tint = @color/control_checkable_material：圆环外径 20、环宽 2、内点直径 10，颜色随选中状态（出处：Android SDK 平台资源 data/res/drawable/btn_radio_on_mtrl.xml（按应用的 compileSdk 取对应平台））
- 实测单选行 48dp，圆环 20dp、环宽 2dp、内点 10dp，标签 18sp；改成自绘行后与源端一致：修好后的写法（出处：卡里修好并验证过）
针对本应用要查的：
- 选中色和未选色：源工程 res/values 下的 styles/themes XML，按应用主题的 colorAccent、colorControlNormal 找；选中用 colorAccent，未选用 colorControlNormal 的值；主题没写的沿父主题找到平台值
来源：1 张卡，1 个应用
- case-dadda7b6820516f5f415（Privacy Friendly 2048）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2、诊断；取值 4 ← 诊断

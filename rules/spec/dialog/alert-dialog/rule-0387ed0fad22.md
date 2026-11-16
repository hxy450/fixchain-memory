# AlertDialog 外观来自主题继承的平台样式时，规格从平台资源取值写成数值契约

审的是：规格
触发（任一种）：
- 读到：AlertDialog.Builder（含 DialogFragment.onCreateDialog 里的）没有自定义样式，应用主题继承 android:Theme.Holo 这类平台主题；写错的样子：契约只写标题对齐、按钮槽位、遮罩和可取消性，或写「按平台默认」「暗底白字」，没有标题字号颜色、分隔线、消息字号、按钮条、窗口背景、宽度和进出场
- 读到：AlertDialog.Builder 没有 setView，应用主题继承 Theme.Holo 或 Theme（targetSdk ≤ 20，或 values-v11/v14 主题继承它们）；写错的样子：按钮顺序、等分还是靠右、大小写、面板底色的依据只到 themes_*.xml 或凭记忆（「平台缺省」），没有布局文件锚点；或没写遮罩浓度
适用范围：源端默认 AlertDialog 外观全靠 Theme.Holo 等平台主题、目标自绘复刻时，规格的对话框可见契约
做法：
- 顺「应用主题 → alertDialogTheme / alertDialogStyle → layout → 布局文件」读平台资源，逐项写数值和资源名：标题样式与 titleDivider、消息字号、窗口背景 drawable、宽度 windowMinWidthMinor / Major（减框体内边距）、进出场
- 按钮条读 buttonPanel 的先后、layout_gravity、layout_weight 定顺序和等分（button1 正、button2 负），写按钮字号、高度和分隔线；写遮罩浓度 backgroundDimAmount，多个对话框叠放时只暗一次
- 每个对话框单列 setCancelable；标题按平台样式写颜色；只凭主题文件或记忆裁定的标待核
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Theme.Holo：alertDialogTheme = Theme.Holo.Dialog.Alert，alertDialogStyle = AlertDialog.Holo，backgroundDimAmount = 0.6：Theme.Holo 下对话框样式和遮罩浓度的出处（出处：Android SDK 平台资源 data/res/values/themes_holo.xml，Theme.Holo（按应用的 compileSdk 取对应平台））
- Theme.Holo.Dialog.BaseAlert 的 windowTitleStyle = DialogWindowTitle.Holo；TextAppearance.Holo.DialogWindowTitle：textSize 22sp，textColor @color/holo_blue_light（#ff33b5e5）：Theme.Holo 下对话框标题的字号和颜色（出处：Android SDK 平台资源 data/res/values/themes_holo.xml，Theme.Holo.Dialog.BaseAlert；styles_holo.xml，TextAppearance.Holo.DialogWindowTitle；colors_holo.xml，holo_blue_light（按应用的 compileSdk 取对应平台））
- AlertDialog.Holo：layout = @layout/alert_dialog_holo，fullDark = @drawable/dialog_full_holo_dark（topDark/centerDark/bottomDark 同为 dialog_*_holo_dark）：Holo 对话框的布局和面板 drawable（出处：Android SDK 平台资源 data/res/values/styles_holo.xml，AlertDialog.Holo（按应用的 compileSdk 取对应平台））
- alert_dialog_holo：titleDivider 高 2dip、背景 holo_blue_light；buttonPanel 依次是 button2（layout_gravity=start）、button3（center_horizontal）、button1（end），每个 layout_weight="1"；button1 是正键、button2 是负键：标题下的蓝线；Holo 下负键在左、正键在右、整条等分，不是靠右（出处：Android SDK 平台资源 data/res/layout/alert_dialog_holo.xml，titleDivider、buttonPanel（按应用的 compileSdk 取对应平台）；com.android.internal.app.AlertController#setupButtons）
- 消息 TextView 用 ?android:attr/textAppearanceMedium；Theme.Holo 下是 TextAppearance.Holo.Medium → TextAppearance.Medium，textSize 18sp：消息字号（出处：Android SDK 平台资源 data/res/layout/alert_dialog_holo.xml，message；themes_holo.xml、styles.xml，TextAppearance.Medium（按应用的 compileSdk 取对应平台））
- dialog_min_width_minor = 95%，dialog_min_width_major = 65%：windowMinWidthMinor / Major：竖屏取窗口宽的 95%、横屏 65%（出处：Android SDK 平台资源 data/res/values/dimens.xml，dialog_min_width_minor、dialog_min_width_major（按应用的 compileSdk 取对应平台））
- params.dimAmount 取窗口主题的 backgroundDimAmount（缺省 0.5f）：变暗是窗口层的效果，浓度来自主题（出处：com.android.internal.policy.PhoneWindow#generateLayout）
- Holo 面板单色 #282828，按钮条 53.33dp 带分隔线，两键两等分、单键占满；面板宽 = 窗口宽 ×（竖 0.95 / 横 0.65）− 32；两层对话框背景只暗一次 0.6：返修按平台资源与安卓实测取得的值（出处：卡里修好并验证过）
针对本应用要查的：
- 应用主题继承的是哪个框架主题，以及它的对话框样式：源工程 AndroidManifest 的 android:theme，以及 res/values*/styles.xml（含 values-v11、values-v14）里这个主题的 parent 链；再到 Android SDK 平台资源 data/res/values/themes*.xml 找该平台主题的 alertDialogTheme、alertDialogStyle；顺着 windowTitleStyle → textAppearance、alertDialogStyle → layout 和面板 drawable、windowMinWidthMinor / Major → dimens、backgroundDimAmount 读出各项数值；例：Theme.Holo 下是 AlertDialog.Holo、alert_dialog_holo、0.6
未核实：Holo 默认对话框按钮是混合大小写：卡里返修实测的样式没提大小写，只在针对出事应用的建议里按布局写成混合大小写
来源：2 张卡，2 个应用
- case-20015832edaeb45f53bb（Bubble Shooter）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1、诊断；做法第 3 步 ← 建议 1；取值 8 ← 诊断
- case-ed0c3a60e7342aa867b4（Blockinger）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 1；取值 8 ← 诊断

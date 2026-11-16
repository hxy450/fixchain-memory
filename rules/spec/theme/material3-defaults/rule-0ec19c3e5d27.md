# 规格记录 Material3 主题基底时，一并写出对话框与底部面板的圆角、底色、宽度、遮罩契约

审的是：规格
触发（任一种）：
- 读到：源工程 styles.xml 的应用主题继承 Theme.Material3.*，源码用 MaterialAlertDialogBuilder、BottomSheetDialog；写错的样子：设计文档主题系统节只记了 Material3 继承树，没有对话框和底部面板的圆角、底色、宽度、遮罩数值；页面规格的映射行只写「MaterialAlertDialog → showAlertDialog / CustomDialog」，不引用外观契约
适用范围：规格提取阶段的设计文档主题系统节和页面规格的对话框映射行
做法：
- 主题系统节写对话框契约：圆角 28、底色取 colorSurfaceContainerHigh 的解析值（浅、深色）、宽度为窗宽减 48vp 并限制在 280–560vp、遮罩为源主题 backgroundDimAmount 的黑；底部面板同样写出
- 页面规格的 MaterialAlertDialog 映射行引用这份契约，并写明弹层形态（居中 openCustomDialog 或 bindSheet）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- MaterialAlertDialog.Material3：backgroundTint = ?attr/colorSurfaceContainerHigh，shapeAppearance = ?attr/shapeAppearanceCornerExtraLarge（28dp）：M3 对话框的底色和圆角（出处：com.google.android.material:material 包内 res/values/values.xml，MaterialAlertDialog.Material3（按应用依赖的版本））
- m3_comp_scrim_container_opacity = 0.32：M3 对话框遮罩不透明度（出处：com.google.android.material:material 包内 res/values/values.xml，m3_comp_scrim_container_opacity（按应用依赖的版本））
- mtrl_alert_dialog_background_inset_start / _end = 24dp：宽度要减去的左右缩进（出处：com.google.android.material:material 包内 res/values/values.xml，mtrl_alert_dialog_background_inset_start（按应用依赖的版本））
针对本应用要查的：
- colorSurfaceContainerHigh 的解析值：源工程 res/values 与 values-night 下 styles / themes 里应用主题的覆写；没覆写时查 Material 库 Theme.Material3.Light / Dark；顺着 @color/… 解析到浅色、深色两个 #RRGGBB 写进契约
未核实：280–560dp 的宽度上下限在 Material 库资源里没查到对应 dimen，按卡写
来源：1 张卡，1 个应用
- case-9c819765c4d3d422d7bb（AntennaPod）：做法第 1 步 ← 建议 5、建议 1；做法第 2 步 ← 建议 5、建议 3

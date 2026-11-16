# AlertDialog.setView 对话框的可见契约写进遮罩浓度和卡片限高，并写明由宿主哪个参数承载

审的是：规格
触发（任一种）：
- 读到：源端 android.app.AlertDialog.Builder 的 setView / setTitle / setPositiveButton，没有改窗口 dim；写错的样子：规格的可见契约只写框体、标题、按钮条、宽度，没有遮罩浓度和高度上限，也没写哪几项由宿主的 openCustomDialog 参数承载
适用范围：规格提取阶段为框架 AlertDialog（含 setView 自定义视图）写可见契约时
做法：
- 契约里写遮罩浓度（取运行期主题的 backgroundDimAmount）和卡片高度上限（窗口夹在系统栏之间，对话框背景 inset 上下各留白，超高时内容视图缩短、框内滚动），与标题、按钮条、框体、宽度并列
- 写明由宿主 openCustomDialog 的哪几个参数承载（如遮罩 maskColor、对齐、点外部取消），哪几项由内容组件自己实现
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Theme.Material.Light 的 backgroundDimAmount 是 0.6：运行期主题是 Material 浅色时的遮罩浓度（出处：Android SDK 平台资源 data/res/values/themes_material.xml，Theme.Material.Light 的 backgroundDimAmount（按应用的 compileSdk 取对应平台））
- dialog_background_material 的 android:inset 是 16dp：对话框背景上下左右各留 16dp，限高时要扣掉（出处：Android SDK 平台资源 data/res/drawable/dialog_background_material.xml（按应用的 compileSdk 取对应平台））
- BaseDialogOptions.maskColor 默认 0x33000000：不写时目标遮罩比 0.6 浅得多（出处：js-apis-promptAction.md，BaseDialogOptions）
针对本应用要查的：
- 运行期主题：源工程清单里 Activity / application 的 android:theme 和 values-v21 等限定目录下的主题定义；顺父主题找到提供 backgroundDimAmount 的平台主题，读出数值
来源：1 张卡，1 个应用
- case-9d195db79dc4cccc7d1a（Sokoban）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1

# 只靠平台默认外观的 AlertDialog（含 DialogPreference 弹出的偏好对话框）迁移前写出完整可见契约：标题字号色与标题线、消息、按钮条与按钮集合、框体、宽度规则与进出场从源主题的平台资源取值；按钮按角色核对槽位，要求一比一时用共享自定义弹窗复刻；按钮排位与面板读对话框样式的 layout 资源，返回键与点外部两条取消路径分别核对

ID：`lesson-9c4de55af3c1ecd8eaa4` · 版本：5

[本主题](index.md)

## 何时使用

规格提取阶段为源端系统对话框（代码中 AlertDialog.Builder 构造，或 PreferenceActivity 中 EditTextPreference、ListPreference 等点击弹出）写转换决策时，以及界面实现阶段按该决策落地 ArkUI 系统弹窗或自定义弹窗时；规格整合时在几条来源之间裁定按钮排位、面板样式与取消方式时；页内复刻多个同时显示的对话框、安排遮罩与遮罩点击时

## 适用情境

源码用 AlertDialog.Builder 内联构造确认框，只设 title、message、setPositiveButton、setNegativeButton，无自定义布局或样式，外观由应用主题继承的平台默认警告框决定；目标准备用 ArkUI AlertDialog.show(primaryButton/secondaryButton) 等系统弹窗替代，项目要求与源端逐屏一致。 也包括应用主题为 Theme.Holo 等框架主题，多个对话框都由 Builder 或 DialogPreference 构造、没有自定义样式；规格只按经验摘要写了“标题左对齐、负左正右、遮罩、cancelable”几项，各页写者凭记忆或兄弟页先例自绘面板。 也包括 targetSdk≤20 或 values-v11/v14 中应用主题继承 Theme.Holo/Theme 的旧应用：Builder 未调用 setCancelable、setCanceledOnTouchOutside，源端可能同时叠放两个以上对话框；目标用页内遮罩加自绘面板复刻，同时要防止点击穿透到下层画面。

## 例外与边界

- 项目明确接受目标系统弹窗的固有外观、只要求文案与按键行为一致；此时仍按角色核对按钮槽位

## 原因

“正/负”是按钮角色，不是参数次序。ArkUI AlertDialog 把 primaryButton 放在左侧，自带居中标题、大圆角卡片、首字母大写的彩色按钮与全窗居中；安卓平台默认警告框的外观随对话框主题而异：AppCompat Light 主题下的 Material 警告框标题左对齐、按钮靠右、负键在左正键在右、全大写、小圆角；Theme.Holo 的 alert_dialog_holo 布局把 button2、button3、button1（负、中、正）按 layout_weight=1 等分排开，按钮不全大写，面板取单色的 dialog_*_holo_dark（本机 SDK android-30 res/layout/alert_dialog_holo.xml、values/styles_holo.xml）。遮罩浓度与进出场取自平台主题。只写“系统组件 1:1/行为等价”时规格没有视觉契约，转换者照映射参考直接替换，版式与按钮顺序整体偏离。可见契约只写槽位与遮罩时，标题颜色与字号、标题分隔线、消息字号、按钮条、框体与宽度仍没有来源。另一应用（Theme.Holo）的四个对话框被写成白色 20fp 标题、无蓝线、圆角描边、320vp 封顶；偏好对话框被当作普通自定义弹窗，ListPreference 还漏了平台默认的 Cancel。 按钮排位、等分或靠右、大小写与面板底色写在主题 alertDialogStyle 指向的对话框样式里（layout 属性指向的布局，fullDark/topDark/centerDark/bottomDark 等面板 drawable），themes_*.xml 只给出这个引用；只读主题文件、或凭“哪一代平台改过按钮顺序”的记忆裁定，契约会混进另一代主题的特征。取消有两条互相独立的默认路径：返回键（Dialog 的 mCancelable 默认 true）与点窗口外部（未调用 setCanceledOnTouchOutside 时，targetSdk≥11 读对话框主题的 windowCloseOnTouchOutside；Holo 对话框主题指向 config_closeDialogWhenTouchOutside，values/config.xml 中为 true；本机 android-36.1 源码 PhoneWindow.java、Dialog.java 与 android-30 res）。只写返回键时，规格会写成“仅返回键关闭”，实现就用吞点击的遮罩。多个对话框同时显示时变暗是窗口层效果，只暗一次（Theme.Holo 两层对话框的参照机实测）；每个面板各画一层遮罩会叠加加深。 布局资源只给初值：Material 对话框布局里 visibility=gone 的 Space（titleDividerNoCustom、textSpacerNoTitle、textSpacerNoButtons）由 AlertController.setupView 按有无标题、消息或列表、setView 自定义视图、按钮切换显隐，单行的 DialogTitle 在放不下时由 onMeasure 改成小一号字两行；只读 XML 会把运行期显示的标题间隔判成“平台不显示”。对话框还是独立窗口：dim 覆盖整块屏幕（源主题由应用窗口绘制状态栏底色时连状态栏一起压暗），窗口在状态栏与导航栏之间居中；契约只写“遮罩浓度、居中”时，这两个参照都会丢。

## 做法

1. 按源端实际使用的对话框类与应用主题定位平台样式（例如框架 android.app.AlertDialog 在 AppCompat Light 主题下取平台 Theme.Material.Light.Dialog.Alert，Theme.Holo 下取 Holo 对话框样式），从本机 SDK platforms/android-<api>/data/res 读取并写成数值契约：标题样式与 titleDivider（Holo 为 22sp #33B5E5 加 2dp 线）、消息字号、按钮条（分隔线、按钮字号、高度与大小写）、按钮排位、窗口背景（9-patch 或圆角）、宽度规则（windowMinWidthMinor/Major，Holo 竖 95%、横 65% 再减框体内边距）与高度上限（对话框窗口夹在系统栏之间，对话框背景 inset 上下各留白；内容超高时自定义视图或消息区缩短并在框内滚动，标题与按钮条保持可见）、遮罩浓度与覆盖范围（源主题由应用窗口绘制状态栏底色时 dim 连状态栏一起压暗）、显示位置与参照区（源对话框窗口在状态栏与导航栏之间居中）、进出场，以及每个对话框的 setCancelable 与返回键行为；每项注明资源路径。目标用 openCustomDialog 且窗口非全屏时，契约同时写出目标侧处理：弹窗期间切换状态栏底色、按顶部与底部避让差的一半下移卡片。 布局里 visibility=gone 的 Space 与 DialogTitle 等框架控件的单行属性只是初值：间隔是否显示看本机 SDK sources/android-<api> 的 AlertController.setupView（有标题且有消息或列表、无自定义视图时显示 titleDividerNoCustom；有 setView 自定义视图时标题下无间隔；消息区 Space 随 contentPanel 隐藏），标题缩字看 DialogTitle.onMeasure，或按参照机实测，按槽位组合分别写进契约，不以 XML 的 gone 判定“平台不显示”；按钮高度取实测或完整样式链结果，不把按钮 minHeight 当渲染高度。 按钮排位、按钮条等分或靠右、大小写与面板底色从主题 alertDialogStyle 指向的对话框样式取：其 layout 指向的布局里 buttonPanel 各按钮的顺序、layout_gravity、layout_weight，以及 fullDark/topDark/centerDark/bottomDark 面板 drawable（例：Holo 为 values/styles_holo.xml 的 AlertDialog.Holo → layout/alert_dialog_holo.xml）；遮罩浓度取主题 backgroundDimAmount。取消契约同时写点对话框外部：源码未调用 setCanceledOnTouchOutside 时，沿实际对话框主题的父链（如 Theme.Holo.Dialog.Alert → Theme.Holo.Dialog）找 windowCloseOnTouchOutside，再解析它引用的 values/config.xml 布尔值（targetSdk≥11 才生效）；返回键与点外部分别写明关闭哪一层、关闭后的状态，源码没有显式 setCancelable(false) 或 setCanceledOnTouchOutside(false) 时不写“仅返回键可关”。点外部取消写出实际判定：只有这次触摸没有被对话框窗口内的视图消费（按钮、列表、输入框、可滚动正文、按钮条都会消费按下）且抬起落在窗口外才取消（Dialog.dispatchTouchEvent 先交窗口视图，未消费才进 onTouchEvent → Window.shouldCloseOnTouch；本机 SDK sources/android-<api> 的 Dialog.java、Window.java）；按在这些控件上拖到外部松手不取消，按在标题等不消费触摸的位置拖出或直接点外部才取消。
2. 映射按钮时先查目标弹窗把每个参数槽位放在哪一侧，再按角色和视觉位置决定正/负键放进哪个槽位。
3. 目标系统弹窗的固有版式与源端对不上而任务要求一比一时，规格直接决定用自定义弹窗（openCustomDialog 加自绘面板）复刻；实现阶段若规格只写了“系统弹窗 1:1”，先与源端截图或平台样式逐项比对，有差异就回报规格或改用自定义实现。
4. DialogPreference 弹出的对话框与代码构造的对话框同等写入契约：按钮集合按框架默认推导（DialogPreference 默认 OK/Cancel，XML 写了 positive/negativeButtonText 用字面值；ListPreference 去掉 positive、点项即写入并关闭、只留 negative），未写的按钮文案取平台 ok/cancel 字符串并按源端语言建多语言资源；内容布局取平台 preference_dialog_edittext、select_dialog_singlechoice_*；EditTextPreference 打开即聚焦并按 numeric/inputType 弹对应键盘。
5. 多个对话框共用同一平台外观时实现一个共享弹窗组件（标题区、可滚动消息、内容槽、按钮条、框体、宽度规则、进出场，cancelable 作参数），各页只传标题、消息、内容与回调；规格只写“按平台默认”而没有数值时，实现者先读平台资源或回报规格缺项，不凭记忆、兄弟页先例或魔法数字报告填值。 面板容器自身设底色，契约里标题、消息、按钮条各区的底色逐一落到对应容器，声明过的颜色常量都要有引用。
6. 源端会同时显示多个对话框时，页内复刻由宿主根统一画一层遮罩（浓度取主题 backgroundDimAmount，不复用应用里碰巧存在的半透明颜色资源），面板组件只画面板，叠放与关闭顺序由宿主的对话框栈管理。遮罩点击按点外部取消契约处理：可取消就关闭最上层，并与返回键共用同一取消处理；源端不可取消时才只拦截点击。用 openCustomDialog 的 autoCancel 或 onWillDismiss(DismissReason.TOUCH_OUTSIDE) 承载点外取消时，系统按抬起点判定、不看按下点：给会消费触摸的区域挂 onTouch，按下时登记、抬起或取消后在本次事件处理完再清除，TOUCH_OUTSIDE 分支先排除已登记的触摸，返回键路径不受影响。自己对平台默认的判断与规格冲突时写进 handback 的 decision_gaps，不按较窄的规格实现，也不在注释里把规格的限制写成源端语义。
7. 规格整合阶段在几条来源之间裁定按钮排位、大小写或取消方式时，只有带资源文件或行号回执的结论算查证：没有锚点的参考文档句子、只读主题文件或凭平台版本记忆得出的结论，都回到第 1 步的布局与主题资源核对；被判为误记的来源，其余片段也核对后再留在契约里，账本依据栏只写确实打开过的文件。

来源支持：9 张卡 · 4 次迁移 · 4 个应用

## 来源（按需复核）

- [case-20015832edaeb45f53bb](../../../../store/cases/case-20015832edaeb45f53bb/c5b354b6bb37ff1dccf5f009e901cc7aa26ff2d922b0dd77dda899f9632e66a4.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:4, recommendation:5
  卡片版本：`c5b354b6bb37ff1dccf5f009e901cc7aa26ff2d922b0dd77dda899f9632e66a4`
- [case-21e1e83afaa8d814dc37](../../../../store/cases/case-21e1e83afaa8d814dc37/ca414833340bf1b9bc1cc58bf84fee86761e2d34439da34c71d729729161668a.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`ca414833340bf1b9bc1cc58bf84fee86761e2d34439da34c71d729729161668a`
- [case-5056fd5bebd86cb55f92](../../../../store/cases/case-5056fd5bebd86cb55f92/9f7f4eea6d10982480411eb8944ad17142de59175bbc8279e080883f95919c6b.json) · 结论：recommendation:2, recommendation:5
  卡片版本：`9f7f4eea6d10982480411eb8944ad17142de59175bbc8279e080883f95919c6b`
- [case-5b8257f101e304280326](../../../../store/cases/case-5b8257f101e304280326/164d1cbeb11290a96f31f9f35177938c28226a4ec54c8365397e5da180b2ec6a.json) · 结论：diagnosis, recommendation:1, recommendation:4, recommendation:5
  卡片版本：`164d1cbeb11290a96f31f9f35177938c28226a4ec54c8365397e5da180b2ec6a`
- [case-8539606efd3a93a5fcb0](../../../../store/cases/case-8539606efd3a93a5fcb0/af76f1f76eaf0311c2a30b87184083e11cab66893b16fe505d8c8563aee2185a.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:4, recommendation:5
  卡片版本：`af76f1f76eaf0311c2a30b87184083e11cab66893b16fe505d8c8563aee2185a`
- [case-96bad1fc979bd25d24d3](../../../../store/cases/case-96bad1fc979bd25d24d3/e9aae85b3c4653261a6cb758cbd6089a333eeb7fde4380278a15e24aa285615e.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`e9aae85b3c4653261a6cb758cbd6089a333eeb7fde4380278a15e24aa285615e`
- [case-9d195db79dc4cccc7d1a](../../../../store/cases/case-9d195db79dc4cccc7d1a/3ef58b6e05f43ead616304c92324166e074aa81e33e4c6ecad7b4910b60126e9.json) · 结论：diagnosis, recommendation:1, recommendation:3, recommendation:4, recommendation:8
  卡片版本：`3ef58b6e05f43ead616304c92324166e074aa81e33e4c6ecad7b4910b60126e9`
- [case-bee1ccf417ac7e3b453c](../../../../store/cases/case-bee1ccf417ac7e3b453c/068040f8788f96fdef9193826f1b953f434b4436bdfe72355d6b81975952282b.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`068040f8788f96fdef9193826f1b953f434b4436bdfe72355d6b81975952282b`
- [case-ed0c3a60e7342aa867b4](../../../../store/cases/case-ed0c3a60e7342aa867b4/72a121533a777b3f391b3c19ced6417310c07f19590b2c0971726410e40c7715.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`72a121533a777b3f391b3c19ced6417310c07f19590b2c0971726410e40c7715`

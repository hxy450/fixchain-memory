# ui/dialog/appearance

弹窗外观与窗口几何：只靠平台默认外观的 AlertDialog 的可见契约与按钮角色槽位，MaterialAlertDialog 按主题代际的卡片外观与遮罩，三方库或 Dialog 主题决定的窗口宽度公式与遮罩、点外关闭、底色圆角，非全屏窗口下 openCustomDialog 的遮罩与状态栏，bindPopup 气泡的整体着色

[上一级](../index.md)

## 本级经验

- [MaterialAlertDialog 卡片外观按源主题代际取值，每个弹层显式设置取自源主题的遮罩](lesson-39077e6612d5f97b0731.lesson.md)
  - 时机：界面实现与规格提取阶段，把 MaterialAlertDialogBuilder 对话框转换为 ArkUI 自绘卡片或弹层，确定卡片宽度、圆角、底色与遮罩时
  - 情境：应用主题继承 Theme.Material3.*（或 MaterialComponents），对话框由 MaterialAlertDialogBuilder 构建；目标用 openCustomDialog、bindSheet 或页内遮罩自绘，工程中有被当作族先例的卡片，可能登记了按 M2 推断的近似值。
- [只靠平台默认外观的 AlertDialog（含 DialogPreference 弹出的偏好对话框）迁移前写出完整可见契约：标题字号色与标题线、消息、按钮条与按钮集合、框体、宽度规则与进出场从源主题的平台资源取值；按钮按角色核对槽位，要求一比一时用共享自定义弹窗复刻；按钮排位与面板读对话框样式的 layout 资源，返回键与点外部两条取消路径分别核对](lesson-9c4de55af3c1ecd8eaa4.lesson.md)
  - 时机：规格提取阶段为源端系统对话框（代码中 AlertDialog.Builder 构造，或 PreferenceActivity 中 EditTextPreference、ListPreference 等点击弹出）写转换决策时，以及界面实现阶段按该决策落地 ArkUI 系统弹窗或自定义弹窗时；规格整合时在几条来源之间裁定按钮排位、面板样式与取消方式时；页内复刻多个同时显示的对话框、安排遮罩与遮罩点击时
  - 情境：源码用 AlertDialog.Builder 内联构造确认框，只设 title、message、setPositiveButton、setNegativeButton，无自定义布局或样式，外观由应用主题继承的平台默认警告框决定；目标准备用 ArkUI AlertDialog.show(primaryButton/secondaryButton) 等系统弹窗替代，项目要求与源端逐屏一致。 也包括应用主题为 Theme.Holo 等框架主题，多个对话框都由 Builder 或 DialogPreference 构造、没有自定义样式；规格只按经验摘要写了“标题左对齐、负左正右、遮罩、cancelable”几项，各页写者凭记忆或兄弟页先例自绘面板。 也包括 targetSdk≤20 或 values-v11/v14 中应用主题继承 Theme.Holo/Theme 的旧应用：Builder 未调用 setCancelable、setCanceledOnTouchOutside，源端可能同时叠放两个以上对话框；目标用页内遮罩加自绘面板复刻，同时要防止点击穿透到下层画面。
  - 例外：项目明确接受目标系统弹窗的固有外观、只要求文案与按键行为一致；此时仍按角色核对按钮槽位
- [对话框几何由三方库或 Dialog 主题决定时，自绘窗口宽度按提供方公式计算并随窗口重算，不写容器 100%](lesson-dcd9ca5a3ac384a1b6b7.lesson.md)
  - 时机：规格提取与界面实现阶段，为三方库对话框封装（如 material-dialogs）、MaterialAlertDialog 或 Dialog 主题 Activity 改成的卡片页确定窗口宽度，以及遮罩、点外关闭、底色与圆角等窗口属性时
  - 情境：源码只出现库的 Builder、库名或 manifest 的 Theme.*.Dialog 主题，源码树里没有宽度等数值；目标用 openCustomDialog 自绘，或把 Dialog 主题 Activity 做成 NavDestination 卡片页，需要显式给出卡片宽度；同族页面或共享弹窗组件可能已按 width('100%')、固定比例或工程里现成的半透明颜色资源写成先例。
- [整体着色的气泡用 bindPopup 的 popupColor，而不是只给内容加背景](lesson-05dc4eb9548bf3fef6ae.lesson.md)
  - 时机：界面实现阶段，把 Balloon、Tooltip 等带箭头的气泡迁移为 bindPopup 自定义 builder 时
  - 情境：源 setBackgroundColor 作用于整个气泡（含箭头），目标的箭头与外框由 popup 容器绘制。
- [非全屏窗口用 openCustomDialog 承载源对话框窗口时，遮罩压不到系统绘制的状态栏、卡片按整窗居中：弹窗期间按 dim 切状态栏底色，按避让差下移卡片](lesson-4f60c8233a03d4676c92.lesson.md)
  - 时机：界面实现阶段，用 openCustomDialog（或其他系统弹窗）承载 Android 对话框、确定遮罩与显示位置参数时，包括共享弹窗工具与各页宿主的打开处
  - 情境：源主题由应用窗口绘制状态栏底色（Theme.Material 及以后 windowDrawsSystemBarBackgrounds=true、statusBarColor 不透明），对话框窗口 dim（主题 backgroundDimAmount，Material 为 0.6）覆盖整块屏幕，窗口在状态栏与导航栏之间居中；目标窗口保持非全屏，状态栏由系统按 statusBarColor 绘制，对话框用 openCustomDialog 加 maskColor 与 DialogAlignment.Center 打开。

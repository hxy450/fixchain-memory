# 框架主题提供勾选图的 CheckBox，目标用平台两态图按 checked 切换，不改用 ArkUI Checkbox

审的是：代码
触发（任一种）：
- 读到：源端 CheckBoxPreference 或 CheckBox 没写 android:button，应用 res 里没有勾选图，勾选图由框架主题的 listChoiceIndicatorMultiple 提供；写错的样子：目标写成 Checkbox().shape(CheckBoxShape.ROUNDED_SQUARE).selectedColor(...) 并自定尺寸，或者给勾选图 Image 用 .fillColor() 二次着色
适用范围：Material 主题（Theme.Material 族）下框架提供勾选图的复选框和复选框偏好项，迁成 ArkUI 时
做法：
- Image(this.checked ? $r('app.media.btn_checkbox_checked_mtrl') : $r('app.media.btn_checkbox_unchecked_mtrl')).width(32).height(32)：尺寸取向量画布 32dp，方框 18dp、圆角 2dp 已在图内；左距取源端布局 widget_frame 的边距
- Image 上加 .accessibilityRole(AccessibilityRoleType.CHECKBOX) 和 .accessibilityChecked(this.checked)，点击仍挂在整行；同页单选标记用同一口径
- 已迁的图颜色不对时，按 tint 链重新烘焙对应状态的文件，或登记资源缺口交资源负责方，不改用 Checkbox
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Widget.CompoundButton.CheckBox 的 button = ?attr/listChoiceIndicatorMultiple；Theme.Material 里 listChoiceIndicatorMultiple = @drawable/btn_check_material_anim，它按 state_checked 选 btn_checkbox_checked_mtrl / btn_checkbox_unchecked_mtrl：框架勾选图的来源链（出处：Android SDK 平台资源 data/res/values/styles.xml，Widget.CompoundButton.CheckBox；data/res/values/themes_material.xml，listChoiceIndicatorMultiple；data/res/drawable/btn_check_material_anim.xml（按应用的 compileSdk 取对应平台））
- btn_checkbox_checked_mtrl：android:width="32dp"、android:viewportWidth="48"，根上 android:tint="@color/control_checkable_material"：Image 尺寸取 32vp，颜色按状态烘焙（出处：Android SDK 平台资源 data/res/drawable/btn_checkbox_checked_mtrl.xml（按应用的 compileSdk 取对应平台））
- Image 32vp 两态切换 + 左距 16 + 无障碍 CHECKBOX 角色和 checked 态后与源端一致；ArkUI Checkbox 圆角约 4vp、勾线偏细，设不成框架样子：返修对照后的结论（出处：卡里修好并验证过）
- accessibilityRole(role: AccessibilityRoleType): T，AccessibilityRoleType.CHECKBOX = 13（@since 18）：给 Image 标成复选框角色（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.accessibilityRole、AccessibilityRoleType.CHECKBOX）
- accessibilityChecked(isCheck: boolean): T（@since 13）：无障碍的勾选状态（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.accessibilityChecked）
针对本应用要查的：
- 应用是否改写了勾选图或用了别的主题族：源工程布局 XML 里这个 CheckBox 的 android:button / style，以及应用主题里的 listChoiceIndicatorMultiple、checkboxStyle；有覆盖时用覆盖的 drawable；主题不是 Theme.Material 族（如 AppCompat、MaterialComponents）时到对应依赖库的 res 里找同名属性指向的图
- 勾选图的左距：源端偏好项或列表项布局里放勾选框的 widget_frame 容器；读出它的 padding / margin（dp），目标写成相同 vp
来源：1 张卡，1 个应用
- case-cec44d314b1979a41843（Sokoban）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2、诊断；做法第 3 步 ← 建议 2；取值 3 ← 诊断

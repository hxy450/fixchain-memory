# 源开关只靠平台默认外观时，目标不用默认外观的 Toggle，按平台资源自绘复刻

审的是：代码
触发（任一种）：
- 读到：SwitchPreference / Switch 没写 android:widgetLayout、style、android:thumb、android:track；写错的样子：写成 Toggle({ type: ToggleType.Switch })，只加 .selectedColor(...) / .switchPointColor(...)，轨道、拇指几何和投影仍是 Toggle 默认
适用范围：源开关外观全部来自框架默认、迁移要求外观与源一致时的 ArkUI 界面实现
做法：
- 对照平台资源核对轨道、拇指、两态颜色和动画，和 Toggle 默认不一致就自绘开关组件：窄胶囊轨道（高 14dp、圆角 7dp，开态 colorControlActivated、关态 colorForeground 的半透明色）+ 比轨道高、外凸的圆拇指（开态 colorControlActivated、关态 colorSwitchThumbNormal，带投影）+ 250ms 拇指位移动画
- 拇指用圆角 Column（borderRadius 取半径）承载 .shadow(...)，让投影随圆形；两态颜色写进目标资源的颜色，设置行改用这个自绘组件
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 轨道 shape：高 14dp、圆角 7dp，左右各内缩 4dp：框架开关的轨道是窄胶囊（出处：Android SDK 平台资源 data/res/drawable/switch_track_material.xml（按应用的 compileSdk 取对应平台））
- 轨道颜色：state_checked → ?attr/colorControlActivated；其余 → ?attr/colorForeground：轨道两态颜色取主题属性（叠加轨道 shape 自身的半透明）（出处：Android SDK 平台资源 data/res/color/switch_track_material.xml（按应用的 compileSdk 取对应平台））
- 拇指 tint：state_checked → ?attr/colorControlActivated；其余 → ?attr/colorSwitchThumbNormal：拇指两态颜色取主题属性（出处：Android SDK 平台资源 data/res/drawable/switch_thumb_material_anim.xml（按应用的 compileSdk 取对应平台））
- THUMB_ANIMATION_DURATION = 250（毫秒）：拇指位移动画时长（出处：android.widget.Switch#animateThumbToCheckedState）
- ToggleType.Switch 默认尺寸 {width:'36vp', height:'20vp'}，拇指半径按组件高度推算、在轨道内：Toggle 默认外观和框架开关不同，只改颜色不够（出处：ts-basic-components-toggle.md，ToggleType枚举说明）
- 拇指 20dp 圆、带投影；用圆角 Column 承载投影后投影随圆形：自绘拇指的尺寸和投影写法（出处：卡里修好并验证过）
针对本应用要查的：
- 主题里 colorControlActivated（Material 主题默认是 ?attr/colorAccent）、colorForeground、colorSwitchThumbNormal 的实际颜色：源工程 AndroidManifest.xml 里 activity 或 application 的 android:theme，顺着 parent 到源工程 res/values 的主题项；没写的落到平台 data/res/values/themes_material.xml 的对应主题；读出颜色，@color 引用解析到 #AARRGGBB。例：Theme.Material.Light 下 colorSwitchThumbNormal 是 switch_thumb_material_light，正常态 #fff1f1f1
来源：1 张卡，1 个应用
- case-01ea7d8b923cd659dbba（Privacy Friendly 2048）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 诊断；取值 6 ← 诊断

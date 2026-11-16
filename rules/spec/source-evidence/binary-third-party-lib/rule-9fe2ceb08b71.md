# 承载 UI 行为的第三方库只映射成 Toast / 自研时，规格写出库的契约字段或登记 PD-*

审的是：规格
触发（任一种）：
- 读到：Gradle 依赖清单里有承载提示条、FAB 菜单、对话框、色板的第三方库（如 de.keyboardsurfer.android.widget:crouton、com.getbase:floatingactionbutton、material-dialogs、HoloColorPicker，常带 @aar）；写错的样子：跨栈映射行只写「promptAction Toast / 自定义 toast 组件」或「ArkUI 自研」一词并标 Auto，没有库本身的队列、时序、尺寸、动画、触摸语义字段，也没登记 PD-*
适用范围：规格提取时，为目标端没有同名库的第三方 UI 库写跨栈映射行
做法：
- 解包本机 Gradle 缓存里该库的 AAR：res/values 读尺寸和样式，classes 用 javap -p -c 读队列、时序和动画常量，写成映射行的契约字段
- 取不到库产物或替代方式要用户定时，按 C8 登记 PD-*（proposed，阻断），由用户改判「占位 / 降级 / 砍 / 换」，不标 Auto
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- crouton：Manager 单队列串行；一条显示 duration + 进入动画时长后移除，退出动画结束再放下一条；有 cancelAllCroutons；不拦截触摸：提示条库要写进契约的语义（按 crouton 1.8.5 解包核对）（出处：卡里修好并验证过）
- getbase FloatingActionsMenu：子钮间距 4dp，标签用库的 9-patch 背景，展开 Overshoot 300ms，加号 0° ↔ 135° 旋转：FAB 菜单库要写进契约的布局和动画值（按 floatingactionbutton 1.10.1 解包核对）（出处：卡里修好并验证过）
针对本应用要查的：
- 库的 AAR 和版本：Gradle 缓存 caches 下 modules-2/files-2.1/<group>/<artifact>/<version>/ 里的 aar，或 transforms 下解包的 transformed/<artifact>-<version>/；res/values/values.xml 读 dimen、style；classes.jar 用 javap -p -c 读常量、动画时长和插值器；按应用依赖的版本取
未核实：卡里的环境是 HarmonyOS 6.1.1（API 24），本机是 API 23
来源：1 张卡，1 个应用
- case-cfa31a0f8f73caf9c2ab（omni-notes-hmos）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1、诊断；取值 1 ← 诊断；取值 2 ← 诊断

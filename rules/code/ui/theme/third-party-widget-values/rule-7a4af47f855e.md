# 输入里出现库的类名或属性时，自研组件照库产物里的布局和动画值写，不自造参数

审的是：代码
触发（任一种）：
- 读到：布局 XML 根元素是 com.getbase.floatingactionbutton.FloatingActionsMenu，带 fab_labelStyle、fab_labelsPosition，子钮 fab_size="mini"；写错的样子：自写的 FAB 菜单组件自定标签圆角和内边距、Column({ space }) 子钮间距、.rotate({ angle: 45 })、OPACITY+scale 过渡时长，都不是库值
- 读到：应用侧常量里有 Configuration.Builder().setInAnimation(…) / setOutAnimation(…)；写错的样子：提示组件的进出动画写成 transition(TransitionEffect.OPACITY.animation({ duration: 150 })) 这类自定时长
适用范围：界面实现时，映射行写「自研 / Toast 替代某库」而输入里出现该库的类名或属性
做法：
- 先定位库产物（Gradle 缓存里的 AAR），解包读 res/values，javap -p -c 读 class，核对布局和动画值后再写组件
- 照库值写：FloatingActionsMenu 子钮间距 4dp、标签用库的 9-patch 背景、展开 Overshoot 300ms、加号 .rotate({ angle: 0 ↔ 135 })；提示条进出动画取 setInAnimation / setOutAnimation 引用的资源
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- getbase floatingactionbutton 1.10.1：子钮间距 4dp、标签 9-patch 背景、Overshoot 300ms、加号 0° ↔ 135°：返修解包 javap 后一比一重写用的库值（出处：卡里修好并验证过）
- rotate(value: RotateOptions): T；RotateOptions.angle: number | string：加号旋转用的通用属性（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.rotate、RotateOptions.angle）
- static rotate(options: RotateOptions): TransitionEffect<"rotate">：同族接口：转场效果里的旋转（出处：鸿蒙 SDK 的 ets/component/common.d.ts，TransitionEffect.rotate）
- animation(value: AnimateParam): TransitionEffect：给转场效果设时长和曲线，时长取库或动画资源里的值（出处：鸿蒙 SDK 的 ets/component/common.d.ts，TransitionEffect.animation）
针对本应用要查的：
- 库的布局尺寸、样式和动画常量：Gradle 缓存 caches 下 transforms 里解包的 transformed/<artifact>-<version>/res/values/values.xml，以及 aar 里的 classes.jar；values.xml 按库前缀（如 fab_）读 dimen 和 style；classes.jar 用 javap -p -c 读动画时长、插值器类和旋转角度常量
未核实：Overshoot 插值器在 ArkUI 里用哪条曲线等价，卡里没写
来源：1 张卡，1 个应用
- case-cfa31a0f8f73caf9c2ab（omni-notes-hmos）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3、诊断；取值 1 ← 诊断

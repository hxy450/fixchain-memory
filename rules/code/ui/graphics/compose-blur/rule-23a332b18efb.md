# Modifier.blur(N.dp) 译成 ArkUI blur 时，半径写成 vp2px(N)，不照搬数字

审的是：代码
触发（任一种）：
- 读到：Modifier.blur(40.dp) 这类带 dp 单位的模糊半径（含图片 Modifier 链调用的自定义 Modifier 扩展函数里的）；写错的样子：.blur(40) 直接照搬数字，没换单位；或者图片上没有 .clip(true)
- 读到：低版本分支在 Coil 请求上挂了位图域的 BlurTransformation(scale = ..., radius = ...)；写错的样子：把 BlurTransformation 的 radius 直接写进组件的 .blur(...)
适用范围：Compose 的 Modifier.blur（含 AsyncImage / Image 上包在自定义 Modifier 扩展里的）译成 ArkUI 组件的 blur 时
做法：
- 写成 .blur(vp2px(N))，N 是源端的 dp 数；模糊包在自定义 Modifier 扩展里时，打开扩展函数的定义取其中 Modifier.blur 的 dp 值
- 图片上的模糊再加 clip：Image(...).blur(vp2px(N)).clip(true)
- 位图域 BlurTransformation 的 radius 是另一套参数，不拿来当组件 .blur() 的半径；半径以 Modifier.blur 的 dp 值换算
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- blur(value: number, options?: BlurOptions): T；最新重载 blur(blurRadius: Optional<number>, options?: BlurOptions, sysOptions?: SystemAdaptiveOptions): T：组件内容模糊，入参是模糊半径，0 不模糊；注释和文档都没写单位（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.blur）
- blur 半径按 px 解释：截图比对后改成 blur(vp2px(N)) 才和源端 Modifier.blur(N.dp) 一致，blur(N) 偏弱；图片上另加 clip：单位按卡里上机结论取（出处：卡里修好并验证过）
- declare function vp2px(value: number): number，@deprecated since 18，@useinstead UIContext#vp2px：把 vp 换成 px 的全局函数，在当前 SDK 里标了废弃（出处：鸿蒙 SDK 的 ets/component/common.d.ts，vp2px）
- clip(clip: Optional<boolean>): T：裁掉模糊溢出组件边界的部分（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.clip）
- backdropBlur(value: number, options?: BlurOptions): T；backdropBlur(radius: Optional<number>, options?: BlurOptions, sysOptions?: SystemAdaptiveOptions): T：同族接口：背景模糊，同样带 BlurOptions，半径同样没写单位（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.backdropBlur）
未核实：blur 半径的单位声明和文档都没写，按 px 是卡里截图比对得出的；case-af4252d474c172e093fc 的上机行为出自 HarmonyOS 6.1.1(24)，本机按 API 23 的声明核实
来源：2 张卡，2 个应用
- case-af4252d474c172e093fc（jerboa）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3、诊断；做法第 3 步 ← 建议 3；取值 2 ← 诊断
- case-f4f67940ef03672d639c（Jetsnack）：做法第 1 步 ← 建议 3、诊断；取值 2 ← 诊断

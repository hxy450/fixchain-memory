# 宿主挂 Material 底部弹层时 bindSheet 显式写 FIT_CONTENT、showClose:false

审的是：代码
触发（任一种）：
- 读到：源端是 BottomSheetDialogFragment，界面里没有关闭按钮和拖拽把手；内容组件头注释写外壳参数归宿主，或给了带 showClose:false 的宿主样例；写错的样子：宿主 bindSheet 的 options 只写了 height、dragBar 或 detents，没写 showClose: false 和 backgroundColor；或者写成 detents: [SheetSize.MEDIUM, SheetSize.LARGE] + dragBar: true；或从邻页锚点块照抄了缺项的 options
适用范围：宿主页把 Material BottomSheetDialogFragment 对应的内容组件挂到 bindSheet 上时
做法：
- 写成 .bindSheet($$this.showSheet, this.sheetBuilder, { height: SheetSize.FIT_CONTENT, dragBar: false, showClose: false, backgroundColor: $r('app.color.…'), maskColor: $r('app.color.…') })，底色和遮罩用源端对应的已迁移颜色资源
- 内容组件头注释给了宿主样例时以样例和源端为准；复用项目里已有的 bindSheet 锚点块前，先对照源 Dialog 核对 height/detents、showClose、dragBar、backgroundColor、maskColor 是否齐全
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- bindSheet(isShow: boolean, builder: CustomBuilder, options?: SheetOptions): T：组件上绑定半模态弹层（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.bindSheet）
- SheetOptions.showClose 默认 true：不写就显示系统关闭 X，源端 BottomSheet 没有（出处：鸿蒙 SDK 的 ets/component/common.d.ts，SheetOptions.showClose）
- SheetOptions.dragBar 默认 true，只在 detents 设了多档并生效时才显示：写多档 detents 时会出现拖拽条，源端没有（出处：鸿蒙 SDK 的 ets/component/common.d.ts，SheetOptions.dragBar）
- SheetOptions.height 默认 SheetSize.LARGE；SheetSize.FIT_CONTENT = 2 为高度自适应内容：不写 height 就是大档（出处：鸿蒙 SDK 的 ets/component/common.d.ts，SheetOptions.height / SheetSize.FIT_CONTENT）
- BindOptions.backgroundColor 默认 Color.White；maskColor?: ResourceColor：弹层底色和遮罩色，不写时不会跟源端主题（出处：鸿蒙 SDK 的 ets/component/common.d.ts，BindOptions.backgroundColor / SheetOptions.maskColor）
- openBindSheet<T extends Object>(bindSheetContent: ComponentContent<T>, sheetOptions?: SheetOptions, targetId?: number): Promise<void>：同族接口：UIContext 上不绑定组件打开半模态，同样用 SheetOptions（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，UIContext.openBindSheet）
- 各宿主补上 showClose:false、改为 FIT_CONTENT + dragBar:false 并统一底色和遮罩后，弹层与源端一致：返修后的写法（出处：卡里修好并验证过）
针对本应用要查的：
- 弹层底色和遮罩色：源工程主题（res/values/themes.xml、styles.xml）里 bottomSheetDialogTheme / bottomSheetStyle 的覆盖；没有覆盖时看应用依赖版本的 com.google.android.material:material 包内 res/values/values.xml 里对应 BottomSheet 样式的 backgroundTint；顺着 ?attr/… 解析到主题里的颜色，再用目标已迁移的同名颜色资源
未核实：卡里的实测分别出自 HarmonyOS 6.1.0（API 23）和 6.0.2（API 22）两个环境
来源：1 张卡，1 个应用
- case-1ff61bb8eea97c7cac7f（AntennaPod）：做法第 1 步 ← 建议 3、建议 5、诊断；做法第 2 步 ← 建议 3、建议 4；取值 7 ← 诊断

# didOverflowHeight 决定展开钮时，目标用 measureTextSize 测两次高度比较

审的是：代码
触发（任一种）：
- 读到：Compose Text 的 onTextLayout { … didOverflowHeight … } 决定是否显示展开/收起按钮，配合 maxLines 切换；写错的样子：目标用字符数阈值判断要不要显示展开钮（如 `.length >` 某个数），没有调用 measureTextSize 之类的实测
适用范围：源 Compose 用文本排版结果（onTextLayout 的 TextLayoutResult）驱动 UI，迁成 ArkUI Text 时；ArkUI Text 没有同名排版回调
做法：
- 用 this.getUIContext().getMeasureUtils().measureTextSize({ textContent, constraintWidth: <Text 实际约束宽度>, fontSize, lineHeight, letterSpacing }) 测不限行高度，同样参数加 maxLines: <源 maxLines> 再测一次；不限行高度 > maxLines 行高度即溢出，显示展开钮
- fontSize、lineHeight、letterSpacing 取源 Text 的同一套 style 值，两次测量只差 maxLines 一项
- 字符数阈值只能作显式标注并登记的临时近似，不作最终实现
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- getMeasureUtils(): MeasureUtils：从 UIContext 取文本测量工具，先取实例再调它的方法（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，UIContext.getMeasureUtils）
- measureTextSize(options: MeasureOptions): SizeOptions：测文本占的宽高，返回的宽和高单位都是 px（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，MeasureUtils.measureTextSize）
- MeasureOptions 的 textContent、constraintWidth?、fontSize?、letterSpacing?、lineHeight?、maxLines?: number：两次测量要传的参数；maxLines 是 MeasureOptions 的正式字段，可以按行数测（出处：鸿蒙 SDK 的 ets/api/@ohos.measure.d.ts，MeasureOptions）
- constraintWidth 默认单位 vp；fontSize 为 number 时按 fp：传入的约束宽度和字号单位；返回值是 px，比较两次高度时同为 px 不用换算（出处：js-apis-measure.md，MeasureOptions）
- Number(noMaxLinesSize.height) > Number(hasMaxLinesSize.height) 即存在截断：官方示例用同样的两次测量判断是否溢出（出处：arkts-apis-uicontext-measureutils.md，measureTextSize 示例2）
- 分别测不限行与 2 行高度并比较，结果决定是否显示展开钮：修复时的做法，复审通过（出处：卡里修好并验证过）
- static measureTextSize(options: MeasureOptions): SizeOptions（MeasureText，@deprecated since 18）：同族接口：旧的静态测量入口，声明写明改用 MeasureUtils#measureTextSize（出处：鸿蒙 SDK 的 ets/api/@ohos.measure.d.ts，MeasureText.measureTextSize）
针对本应用要查的：
- 源 Text 的字号、行高、字距和 maxLines：源工程 Compose 文件里这个 Text 的 style（MaterialTheme.typography 的某一项）和 maxLines 参数；读出 fontSize / lineHeight / letterSpacing 的 sp 值和 maxLines，原样作为两次测量的参数
未核实：卡里的行为出自鸿蒙 SDK API 24，本机核实用的是 API 23
来源：1 张卡，1 个应用
- case-5a84af0e2f5c593b9f0c（Cofi）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；做法第 3 步 ← 建议 2；取值 6 ← 诊断

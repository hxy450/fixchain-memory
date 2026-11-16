# 源端居中 Dialog 带输入框时，目标用页内遮罩加居中卡，不改成 bindSheet

审的是：代码
触发（任一种）：
- 读到：源端用 Dialog / AlertDialog（或自定义 Dialog 子类）inflate 自定义布局弹出居中卡片，根视图点击 dismiss，卡内有输入框；写错的样子：目标在页根挂 .bindSheet(visible, builder, { height: SheetSize.FIT_CONTENT }) 用底部半模态承载
适用范围：为源端弹窗选择鸿蒙承载形态时，按源端 Dialog 类型判断，不按里面有没有输入框判断
不适用的情形：源端是 BottomSheetDialog 一类底部弹窗时才用 bindSheet
做法：
- 居中卡片类 Dialog 用页根 Stack 内 if 条件渲染：半透明遮罩 .onClick 关闭，居中卡片自身加空 .onClick 吞掉点击，卡内按源布局复刻
- 也可用自定义弹窗或 ComponentContent 配 openCustomDialog 承载；不因弹窗里有输入框就默认改成半模态 sheet
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 页根 Stack 条件渲染遮罩加居中白卡，点外关闭、白卡吞点击：卡里修好的承载形态（出处：卡里修好并验证过）
- bindSheet(isShow: boolean, builder: CustomBuilder, options?: SheetOptions): T：给组件绑定半模态页面，是底部弹出形态，不对应居中弹窗（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.bindSheet；ts-universal-attributes-sheet-transition.md，bindSheet）
- openCustomDialog<T extends Object>(dialogContent: ComponentContent<T>, options?: promptAction.BaseDialogOptions): Promise<void>：用 ComponentContent 打开自定义弹窗的另一种承载（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，PromptAction.openCustomDialog）
针对本应用要查的：
- 源端弹窗是哪一类、点外是否关闭：源工程弹窗函数里构造的 Dialog 类，以及它 inflate 的布局 XML 和根视图的点击监听；Dialog、AlertDialog 及其自定义子类按居中卡片处理，BottomSheetDialog 按底部弹窗处理；根视图点击 dismiss 即点外关闭
未核实：openCustomDialog 这条承载出自卡的建议，卡里没上机验证
来源：1 张卡，1 个应用
- case-91f8e7d157380a2457fa（免费来电多多）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；例外 1 ← 建议 1；取值 1 ← 诊断

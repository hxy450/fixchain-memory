# ui/dialog

弹窗与半模态：V2 页面可用的弹窗载体、sheet 内二级弹窗的层级、按源 Dialog 类型选择呈现形态（路由约束不改变弹窗形态）、弹窗内二级选择器的层级、按源布局还原弹窗内容、源 Dialog 用 setView 注入自定义内容时的承载方式

[上一级](../index.md)

## 本级经验

- [@ComponentV2 页面的弹窗不用 CustomDialogController 承载 V2 组件，改用状态驱动浮层、半模态或 openCustomDialog](lesson-3f3e1ff0a4d0e0299bda.lesson.md)
  - 时机：界面实现阶段，为 @ComponentV2 页面选择弹窗承载方式、编写弹窗子组件时（含参照工程内已有弹窗写法时）
  - 情境：项目要求页面与子组件都用 @ComponentV2、不混用 V1；需要把 Android Dialog/DialogFragment 一类居中或底部弹窗迁成 ArkUI；规格可能写着 CustomDialog、@CustomDialog 或 bindSheet。
- [从 bindSheet 半模态里打开的弹窗必须叠在 sheet 之上：不用页内浮层，居中点外可关用模态内自绘遮罩](lesson-009212ca2c691b97d76c.lesson.md)
  - 时机：界面实现阶段，为从底部 sheet 内部触发的二级弹窗（定时、新建输入等）选择承载层时
  - 情境：Android 在 BottomSheetDialog 内再 show 居中 DialogFragment（点外可关）；目标底部弹层用 bindSheet；二级弹窗候选有页内 Stack 条件浮层、bindSheet(CENTER)、bindContentCover 与全局自定义弹窗。
- [按源 Dialog 类型选呈现形态：居中 CustomDialog 用居中卡片，BottomSheetDialog 才用 bindSheet；定长密码框输满即校验](lesson-21db515a505be4845497.lesson.md)
  - 时机：页面接线与界面实现阶段，为源端 DialogHelper 一类函数弹出的确认或输入弹窗选择承载形态与校验触发方式时
  - 情境：源端经 CustomDialog/AlertDialog 加自定义布局弹出居中卡片，卡内可能有定长格子密码框（输满即比对、失败提示），根视图点击关闭；目标公共弹窗封装只有确认/提示类，带输入的弹窗需要在页面内自建。
- [源弹窗按它实际加载的布局 XML 与函数全文逐控件还原，不以行为代码、相邻弹窗外壳或通用确认弹窗代替](lesson-1f366fe4ccdc917ce0fc.lesson.md)
  - 时机：界面转换与接线阶段，为源端弹窗编写或补建 ArkUI 弹窗内容（包括解接线标记时顺带新建弹窗、补齐流程闭环时新建弹窗、考虑复用通用弹窗）时
  - 情境：源弹窗由 ViewBinding/inflate 或工具类加载独立布局（DialogXxxBinding.inflate、R.layout.xxx），含标题、关闭图标、专用图标、说明文字、输入框、单个或多个按钮及容器级 margin；目标工程已有“标题 + 确定/取消”的通用确认弹窗或相邻弹窗写法可参照，或只拿到“展示、复制、关闭”一类功能描述。
- [源确认框用 setView 注入复选框等自定义内容时改用自定义弹窗承载，不写成 AlertDialog.show 的 builder 参数](lesson-18fca50f9c801cb282ec.lesson.md)
  - 时机：界面实现阶段，把 Android AlertDialog/MaterialAlertDialogBuilder 转换为 ArkUI 弹窗、确定弹窗 API 与参数结构时
  - 情境：源对话框在标题、正文和正负按钮之外还 setView 注入自定义布局（如“不再提示”复选框），确认回调读取其中控件的状态并写偏好；目标准备用 AlertDialog.show 弹出。
  - 例外：源对话框只有标题、正文与按钮，没有自定义视图，此时直接映射 AlertDialog.show
- [源端在当前页 show 的底部弹窗保持叠在宿主页上：“路由统一用某框架”只约束页面跳转，不把弹窗改成路由页](lesson-7ef02de8bbc10734c3d2.lesson.md)
  - 时机：规格提取阶段把 Android Dialog/BottomSheet 的呈现方式映射到 ArkUI 承载方式时；界面实现阶段落实弹窗内的二级日历或选择弹层时
  - 情境：Android 入口经 bottomDialog/Dialog 在当前 Activity 上 show 全宽底部面板（遮罩下仍见宿主页、点背景关闭、不入返回栈），面板内再弹同类底部选择器；目标工程有“路由统一使用 HMRouter/Navigation”的约束，且已有同名路由页可复用。

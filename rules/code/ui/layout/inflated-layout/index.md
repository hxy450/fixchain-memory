# inflate / setContentView 加载的弹窗与页面布局

agent 会看到什么：读过的源码里弹窗或二级页由 inflate(R.layout…)、以 Binding 结尾的 ViewBinding 类的 inflate、setContentView 或工具类的 show…Dialog 加载一个布局 XML；交回的目标弹窗或页面是按行为代码、功能描述、通用确认弹窗或 bindSheet 拼出来的

## 规矩

- rule-d4025129fce0｜源端弹窗加载专用布局 XML 时，读完该布局逐项复刻控件，不按行为代码或通用弹窗拼｜读到：源端弹窗由 ViewBinding 类的 inflate(...)、工具方法里的 LayoutInflater.inflate 或 setContentView(R.layout.…) 加载专用布局（标题、ImageView 图标、正文、Button、关闭图标）；计划或审计只给了功能描述，或接线时要解开指向弹窗的 FWD-REF；写错：目标弹窗与源布局 XML 不一致：按行为代码、toast 文案或相邻弹窗外壳拼出，自拟「标题 Text + 文本 + 整宽关闭 Button」的通用结构，或直接调工程现成的通用确认弹窗；缺图标、右上关闭 X、说明文字
- rule-189719e4142c｜源端经工具方法弹窗时，照该方法加载的布局和各按钮分支实现目标弹窗｜读到：源端页面调用工具类的静态方法弹对话框（show…Dialog(this, …) 这类），调用方 lambda 只传了接受回调；被调方法里 inflate 独立布局或 ViewBinding，列表项用 Adapter 渲染；写错：目标弹窗只有标题、Scroll 长文和一个同意 Button，缺列表项和图标、「不同意」按钮、拒绝后的二次确认和退出
- rule-b2e1a4fb8fc5｜源端居中 Dialog 带输入框时，目标用页内遮罩加居中卡，不改成 bindSheet｜读到：源端用 Dialog / AlertDialog（或自定义 Dialog 子类）inflate 自定义布局弹出居中卡片，根视图点击 dismiss，卡内有输入框；写错：目标在页根挂 .bindSheet(visible, builder, { height: SheetSize.FIT_CONTENT }) 用底部半模态承载
- rule-0f8d36d2679f｜二级页由布局 XML 和自定义绘制 View 决定视觉时，读全两者再写，截断就分段重读｜读到：规格映射写明「Activity + 自定义 View → 目标页」，读取回执里布局 XML 和自定义 `View` 的内容落在 `truncated` 截断区，只看到 Activity 里的 `setContentView`、控件 id 和方法调用；写错：目标页结构是自拟的（文字上月/下月、没有星期偏移的 1..N 网格），缺少源端布局和 `onDraw` 画出的圆盘、卡片、月历网格等

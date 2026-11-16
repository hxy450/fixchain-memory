# RelativeLayout 子项的相对规则、贴边和叠放

agent 会看到什么：读到 RelativeLayout（或 FrameLayout）的子 View 带 layout_alignParent*、layout_below、layout_centerVertical、CENTER_IN_PARENT、父容器 android:gravity，或没有任何相对规则；产物里对应的 Column / Row 顺序排列、Row+Blank、Stack 子项上的 .align、Stack 的 alignContent、.position 和 zIndex

## 通用查法

### RelativeLayout 子项迁成 ArkUI 时，逐个读出定位规则再写 Stack 定位

审的是：代码
触发（任一种）：
- 读到：RelativeLayout / FrameLayout 的子 View 带 android:layout_alignParentBottom 等贴边规则、android:layout_gravity，或没有相对规则；写错的样子：目标改成 Column / Row 顺序排列（Blank() 撑开），或 Stack 没写 alignContent、子项上写 .align(Alignment.X) 贴边
适用范围：RelativeLayout / FrameLayout 的子 View 迁成 ArkUI 叠放布局时
做法：
- 按声明顺序列出每个子 View 的定位规则（layout_alignParent*、layout_below、layout_center*、layout_gravity 或无规则）和 margin，及父容器的 android:gravity
- 写成 Stack：显式写 alignContent（Stack 默认居中，源端无规则子项在左上）；贴边子项用 .position({ left/right/top/bottom: 源 margin })，不在子项上写 .align；保持源声明顺序（后声明在上），排不了时补 .zIndex
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- RelativeLayout 里横向、纵向都没有规则的子 View，LTR 下放在左上（RTL 下右上），按自己的 margin 偏移：没有相对规则的几个子 View 叠在同一坐标（出处：android.widget.RelativeLayout#positionChildHorizontal）
- DEFAULT_CHILD_GRAVITY = Gravity.TOP | Gravity.START：FrameLayout 子项不写 layout_gravity 时贴左上（出处：android.widget.FrameLayout#DEFAULT_CHILD_GRAVITY）
- RelativeLayout 带 gravity 时，onMeasure 末尾把全部可见子项（ignoreGravity 指定的除外）作为一组按 gravity 平移：父容器的 gravity 对带 alignParent* 的子项同样生效（出处：android.widget.RelativeLayout#onMeasure）
- StackOptions.alignContent?: Alignment，@default Alignment.Center：Stack 子项默认居中摆放，和源端的左上不同，要显式写（出处：鸿蒙 SDK 的 ets/component/stack.d.ts，StackOptions.alignContent）
- position(value: Position | Edges | LocalizedEdges): T：相对父组件的绝对定位，传 Edges 时按四边距离定位（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.position）
- align(value: Alignment): T：对齐的是组件自己绘制区域里的内容，写在 Stack 子项上不移动子项本身（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.align）
- Stack 的子元素依次入栈，后一个子元素覆盖前一个：声明顺序就是 z 序，和 RelativeLayout 相同（出处：arkts-layout-development-stack-layout.md，概述）
针对本应用要查的：
- 容器里每个子 View 的定位规则、margin 和声明顺序：源工程布局 XML（含 layout-land 等限定目录里的同名布局）里这个 RelativeLayout / FrameLayout 元素和它的直接子元素；逐个子元素读 layout_* 定位属性和 margin，dp 数值按 vp 写进 .position 的对应边或 margin
- 父容器的 android:gravity 和 android:ignoreGravity：同一个布局 XML 里这个容器元素本身的属性；有 gravity 时整组子项按它对齐，用目标容器的 alignContent 表达，不逐个子项钉位置
来源：3 张卡，2 个应用
- case-4f627840679361f165a3（AntennaPod）：做法第 2 步 ← 建议 2
- case-55bbad53c11b2d1b95e6（app_hnaccurateweather_live_android）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3
- case-d53f19cb359b879b340c（AntennaPod）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1

## 规矩

- rule-961454caea13｜RelativeLayout 里没有相对规则的子 View 会叠放，目标用 Stack 叠放，不改成 Column｜读到：RelativeLayout 下几个子 View 都没有 android:layout_below、android:layout_above、android:layout_toRightOf 等相对规则，落在同一块区域（常见于固定高度的 item 里叠放两条曲线）；写错：目标把这些子组件放进 Column 顺序排列、各占一段 height，列被拉长，底部内容被裁切
- rule-a9abefaa72a3｜源子项贴父容器某边时，Stack 子项不用 .align，改父 alignContent 或 .position｜读到：FrameLayout / CoordinatorLayout 子项写 android:layout_gravity（bottom、bottom|end 等），或映射参考写 layout_gravity → .align(Alignment.X)；写错：Stack 子项上写 .align(Alignment.Bottom / BottomEnd)，父 Stack 没写 alignContent
- rule-c5f1920ddd07｜RelativeLayout 子项各锚两端时用 Stack+position，不写 Row+Blank｜读到：RelativeLayout 里一个子项 android:layout_alignParentStart 加 marginStart，另一个 android:layout_alignParentEnd 加 marginEnd，容器定宽；写错：目标写成 Row { Text().margin({ left }), Blank(), Text().margin({ right }) }，两段文字被并排挤开，不像源端那样各自贴边、可能重叠
- rule-cc09073725b7｜RelativeLayout 带 gravity 时子项整组平移，alignParentTop 不抵消居中｜读到：RelativeLayout 设 android:gravity="center_vertical"，子 TextView 同时声明 android:layout_alignParentTop / android:layout_alignParentStart；写错：目标容器写成 Stack().alignContent(Alignment.TopStart)，把子项钉在顶部；理由是 gravity 对带 align 规则的子项无效
- rule-d0caba5fad30｜源端空态挂到根 RelativeLayout 并 CENTER_IN_PARENT 时，目标空态放根 Stack 居中｜读到：空态视图由辅助类 addView 到页面根 RelativeLayout，LayoutParams 上 addRule(RelativeLayout.CENTER_IN_PARENT)；规格 anchors 里列了这个辅助类；写错：空态写在列表所在的子 Stack 或 List 容器里，没有放在页面根 Stack 里居中
- rule-a984e486efcd｜Stack 叠层按源布局声明顺序排 z 序，排不了时补 zIndex｜读到：RelativeLayout 里半透明按钮条先声明，圆角装饰和封面卡后声明（后声明的画在上面）；写错：Stack 里把按钮条放到最后声明，压住封面下沿和圆角装饰，也没有 zIndex
- rule-720b0574d9bf｜RelativeLayout 里在滚动容器外的兄弟视图要放在 Scroll 外，不用 Blank 占位塞进 Scroll｜读到：RelativeLayout 里有兄弟视图位于 ScrollView / NestedScrollView 之外，滚动容器用 android:layout_below="@+id/…" 排在它下面；写错：目标把这个固定视图连同 Blank().height(N) 占位一起放进 Scroll 内的 Column 首部，随内容一起滚动
- rule-8b4cdf4f2a25｜SeekBarPreference 行按源 RelativeLayout 让数值和滑条同起于标题下方叠放，不拆成两行｜读到：SeekBarPreference 的行布局 XML 是 RelativeLayout，数值 TextView 和 SeekBar 都 layout_below 标题、互相重叠；写错：数值 Text 单独占一行，下面再放一个 Slider
- rule-20dc9e33866d｜layout_centerVertical 按钮带 layout_below 标签时，按钮保持源尺寸、标签做下挂层｜读到：RelativeLayout 里按钮 android:layout_centerVertical="true"、尺寸各不相同（如侧键 48dp、主键 64dp），TextView 标签 android:layout_below 指向按钮，兄弟之间有 android:layout_marginStart 等固定 margin；写错：每个按钮连同标签包进统一大小的 Column 槽位竖排居中，带标签的图标被顶高、各键不在同一高度；按钮上源端的 margin 没写
- rule-5e94ddd2b62b｜源控件排里每个 ImageButton / TextView 都要有渲染节点，赋值的展示状态要在 build 里被读｜读到：源布局 RelativeLayout 控件排里 ImageButton 旁有 TextView 标签（android:layout_below 挂在按钮下方的速度、秒数等文字）；写错：目标声明了 @Local / @State 展示状态并在更新函数里给它赋值，build() 里却没有读它的 Text(...)；或注释写着「按钮 + 标签」，对应的 Column 里只有 Image
- rule-9c2b582d4a62｜Stack 里要钉在顶部或角落的子节点用 .position 或父级 alignContent，不用 .align｜读到：MaterialToolbar 带 app:layout_collapseMode="pin" 或 android:layout_alignParentTop 钉在顶部；子 View 用 android:layout_gravity / layout_alignParentBottom 贴父边或角；写错：工具栏写 .align(Alignment.Top)、装饰写 .align(Alignment.BottomStart)，所在 Stack 没设 alignContent，仍被居中

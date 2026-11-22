# Stack 中内容尺寸的子项按 alignContent 定位：子项自身的 .align() 不改变它在父容器中的位置，需要的对齐用满尺寸容器或显式 position

## 何时使用

界面转换与巡检修复阶段，把 Compose 自定义 Layout 或 Box 中的文字改写为 ArkUI Stack 子节点并确定纵向位置时；修复或编译清理删除 height('100%')、.align() 等居中手段时；把 FrameLayout 中按 layout_gravity 叠放的角标、重叠头像翻译成 Stack 时；把 Compose Box 中以 Modifier.align(BottomCenter 等) 定位的子项翻成 Stack 子节点时；把 FrameLayout/CoordinatorLayout 的 layout_gravity、RelativeLayout 的 alignParent*/centerInParent 翻译为 Stack 中 FAB、多选浮层、工具栏、装饰条的定位并确定叠层次序时；把 ConstraintLayout 标题栏（左返回、居中标题、右侧操作）转换为 ArkUI 或抽取公共标题栏组件时

## 适用情境

源端自定义 Layout 用 placeRelative(x, (maxHeight - height) / 2) 把定宽文字纵向居中，或 Box 中文字按居中对齐放置；目标用 Stack({ alignContent: Alignment.TopStart }) 同时容纳文字与图片等对齐需求不同的子项。也包括源端固定尺寸 FrameLayout 中的小角标以 layout_gravity=end|bottom 贴右下，目标写成 Stack({ alignContent: Alignment.TopStart }) 并只给角标加 .align(Alignment.BottomEnd)。也包括源 Box 中部分子项用 Modifier.align 放到非默认位置（如贴底的购买栏），目标 Stack 设了统一的 alignContent(TopStart)，规格写着“底部对齐”。也包括映射参考或兄弟页把 layout_gravity 写成 .align(Alignment.X)，工具栏、浮层、FAB 于是落在父 Stack 中部。也包括标题栏：返回图标约束到父 start、右侧入口约束到 end、标题 0dp 加左右 margin 居中，目标写成 Stack({ alignContent: Alignment.Center }) 并只给返回图标加 .align(Alignment.Start)，后写的页面与公共标题栏组件以它为模板复制。

## 原因

Stack 按 alignContent（或 Stack 自身的 align，二者后设置的生效）放置未撑满的子节点，子项设了 layoutGravity（API 20 起，只对 Stack 的直接子组件生效）时才按子项自己的对齐；Text 的 .align() 只对齐文字在自身框内的位置，内容高的 Text 在 TopStart 的 Stack 里仍落在左上角，ArkUI Alignment 也没有 Compose 的 CenterStart。来源中巡检修复者为裁剪图片把 Row 改成 TopStart 的 Stack，删去 Text 的满高后改写 .align(Alignment.CenterStart) 并自称已居中；编译修复把它改成 Alignment.Start，随后又被删除，分类卡文字一直贴左上。另一应用的成员头像角标照此写成子项 .align(BottomEnd)，角标仍在左上；该片段后来被抽进共享组件继续沿用，直到改成 position 才贴到右下。

## 做法

1. 同一 Stack 中各子项对齐需求不同时，给文字包一个满高容器：Column().width(源端比例).height('100%').justifyContent(FlexAlign.Center).alignItems(HorizontalAlign.Start)，或给子项按源公式单独 position/offset。
2. 删除 height('100%')、.align() 等手段前，确认替代约束仍实现原来的纵向位置；枚举名以 ArkUI SDK 为准，不照搬 Compose 的 Alignment 名称。编译修复把 Compose 专有名（CenterEnd、CenterStart 等）换成 ArkUI 现有名（End、Start）时，若它挂在 Stack 子项的 .align() 上，换名后位置仍不变，同时改为 position 或父 Stack 的 alignContent。
3. 按 layout_gravity 单独对齐某个子项（如 end|bottom 的角标）时，在已知 W×H 的容器里写 position({ x: W - 子宽, y: H - 子高 })，或给该子项单独套一个 alignContent 为对应方向的 Stack。
4. 逐个核对源 Box 子项的 Modifier.align：非默认位置写成 position({ left: 0, bottom: 0 })、markAnchor 等实际属性；规格或报告里的“底部对齐”要落到代码属性上。
5. 子项单向贴边时可改父 Stack({ alignContent })；同一 Stack 内混合对齐用 .position({ left/right/top/bottom })、markAnchor 或满幅透明容器配 justifyContent/alignItems（给这个满幅容器设 hitTestBehavior(HitTestMode.Transparent)，否则默认的 HitTestMode.Default 会挡住下层兄弟节点的触摸和滑动），并保留源 margin。
6. 叠层按源布局声明顺序复核 z 序（后声明者在上），无法按序排列时补 zIndex。
7. 标题栏按约束建互斥的水平槽位：Row 内左侧固定宽槽（宽取标题的 marginStart）放返回入口，layoutWeight(1) 的标题居中，右侧固定槽放操作入口；也可用 RelativeContainer + alignRules 对应 start/end 约束。

## 可选检查

- 沿用了映射参考或先例中的定位写法时，检索 .align(Alignment.，逐个确认它要的是内容对齐还是在父容器中的位置
- 标题栏同时打开返回与右侧入口并用较长标题预览，确认三者不重叠、标题在两侧槽位之间居中

来源支持：11 张卡 · 8 次迁移 · 7 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 源码 android-36.1；androidx.compose.ui:ui-android 1.10.3、1.12.0，androidx.compose.foundation:foundation-layout-android 1.10.3、1.12.0（字节码）。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 5 步〕Stack(options?: StackOptions) 的 StackOptions.alignContent?: Alignment 默认 Alignment.Center，也可用属性 alignContent(value: Alignment): StackAttribute 设；属性与构造参数同时设时以属性为准，与先后无关；alignContent（属性或构造参数）与通用属性 align 同时设时，后设置的覆盖先设置的。Stack 用这一个值摆放全部子组件，非法值按 Center 处理
- 〔原因〕通用属性 align(value: Alignment): T（API 7 起；API 20 起另有重载 align(alignment: Alignment | LocalizedAlignment): T）设置的是本组件绘制区域内子组件（内容）的对齐方式，默认 Alignment.Center，只在 Stack、FolderStack、Shape、Button、Text、TextArea、TextInput、RichEditor、ListItem、GridItem、Scroll 等文档列出的组件上生效；在 Stack 上它与 alignContent 效果一致，只能设置子组件在当前组件内的对齐
- 〔原因〕Text 上的 align 只控制文本段落的纵向位置：TopStart、Top、TopEnd 内容顶部对齐，Start、Center、End 都是垂直居中，BottomStart、Bottom、BottomEnd 底部对齐；Text 不能用 align 控制水平位置，水平由 textAlign 定（未设时 TextAlign.Start，可穿戴设备为 Center）
- 〔原因 / 做法第 3、5 步〕layoutGravity(alignment: LocalizedAlignment): T（API 20 起）单独设置 Stack 中某个子组件的对齐方式，只在父组件为 Stack 时生效，与 align 属性同时使用时 layoutGravity 优先；参数默认 LocalizedAlignment.CENTER，异常值按默认处理。LocalizedAlignment（API 20 起，字符串枚举）成员为 TOP_START、TOP、TOP_END、START、CENTER、END、BOTTOM_START、BOTTOM、BOTTOM_END，按 direction 或系统语言方向镜像
- 〔原因 / 做法第 2 步〕ArkUI 的 Alignment 枚举只有 9 个成员：TopStart(0) 顶部起始端、Top(1) 顶部横向居中、TopEnd(2) 顶部尾端、Start(3) 起始端纵向居中、Center(4)、End(5) 尾端纵向居中、BottomStart(6)、Bottom(7) 底部横向居中、BottomEnd(8)；没有 CenterStart、CenterEnd、TopCenter、BottomCenter 这些名字
- 〔原因 / 做法第 2 步〕Compose 的 Alignment 二维取值都是 BiasAlignment(水平偏移, 垂直偏移)：TopStart(-1,-1)、TopCenter(0,-1)、TopEnd(1,-1)、CenterStart(-1,0)、Center(0,0)、CenterEnd(1,0)、BottomStart(-1,1)、BottomCenter(0,1)、BottomEnd(1,1)（ui 1.10.3 与 1.12.0 相同）；按位置含义 CenterStart 对应 ArkUI 的 Start、CenterEnd 对应 End、TopCenter 对应 Top、BottomCenter 对应 Bottom
- 〔适用情境 / 做法第 4 步〕Compose Box 的 contentAlignment 参数默认 Alignment.TopStart（foundation-layout 1.10.3 与 1.12.0 相同）：调用方没传 contentAlignment、子项也没写 Modifier.align 时，子项贴 Box 左上（RTL 时右上）
- 〔适用情境 / 做法第 3、5 步〕FrameLayout 按每个子项的 layout_gravity 摆放它；子项没写 layout_gravity（值为 -1）时用 DEFAULT_CHILD_GRAVITY = Gravity.TOP | Gravity.START，贴左上（RTL 时 START 在右）。只写了一个方向的 layout_gravity 时，另一方向横向贴左（RTL 下也是左）、纵向贴顶；居中时在居中位置上再整量加 leftMargin − rightMargin（纵向为 topMargin − bottomMargin），贴边时只用靠那一边的 margin
- 〔何时使用 / 做法第 5 步〕RelativeLayout 的子 View 横向、纵向都没有定位规则时，LTR 下放在左上、RTL 下放在右上，按父 padding 和自己的 margin 偏移；centerInParent、centerHorizontal、centerVertical 让子 View 在该方向居中：RelativeLayout 该方向是确定尺寸（EXACTLY）时直接按该尺寸居中；是 wrap_content 等非 EXACTLY 时先暂放在起始边，等 onMeasure 算出自身最终宽（高），按最终尺寸重新居中（alignParentRight、alignParentBottom 的子 View 也在这时按最终尺寸重新贴边）；居中按 RelativeLayout 整个宽（高）算，不扣父 padding，也不计子 View 的 margin
- 〔何时使用 / 做法第 5 步〕RelativeLayout 设了 gravity（不是 start、top 或 0）时，onMeasure 末尾把全部可见子 View（ignoreGravity 指定的那个除外）作为一组按 gravity 平移，带 alignParent* 规则的子 View 也一起平移
- 〔做法第 1、3、4、5 步〕position(value: Position | Edges | LocalizedEdges): T（Position 自 API 7 起，Edges、LocalizedEdges 自 API 12 起）：相对父组件内容区（父尺寸减 border、padding、safeAreaPadding）绝对定位；Position 的 x、y 以内容区左上角为原点，Edges 的 top、left、bottom、right（Dimension）是本组件各边到父内容区对应边的距离，LocalizedEdges 支持镜像。作用在尺寸测量完成之后；父组件为 Row、Column、Flex 时设了 position 的子组件不占位；不支持在宽高为零的布局组件上设置；父组件为 RelativeContainer 且子组件设了 alignRules 时 position 不生效；父组件未设固定宽高时参考第一个设了固定宽高的祖先定位；异常值不生效
- 〔做法第 4、5 步〕markAnchor(value: Position | LocalizedPosition): T 在 position 或 offset 的初始位置上再按锚点偏移：.position({x: a, y: b}).markAnchor({x: c, y: d}) 等于 .position({x: a - c, y: b - d})，offset 同理；单独设 .markAnchor({x, y}) 等于 .offset({x: -x, y: -y})；API 10 起无默认值（API 9 及以前默认 {x: 0, y: 0}），异常值不生效
- 〔做法第 1 步〕offset(value: Position | Edges | LocalizedEdges): T（Edges、LocalizedEdges 自 API 12 起）相对组件原本的布局位置偏移，只在绘制时调整位置、不影响父组件布局；{x, y} 与 {left: x, top: y}、{right: -x, bottom: -y} 效果相同，默认单位 vp；和 position 一起设时 position 生效、offset 不生效
- 〔做法第 1 步〕Column 的 justifyContent(value: FlexAlign): ColumnAttribute 管纵向（主轴）对齐，默认 FlexAlign.Start；alignItems(value: HorizontalAlign): ColumnAttribute 管横向对齐，默认 HorizontalAlign.Center。FlexAlign 成员 Start、Center、End、SpaceBetween、SpaceAround、SpaceEvenly，HorizontalAlign 成员 Start、Center、End；子组件不设 flexShrink 且主轴尺寸之和超过 Column 时，FlexAlign.Center 和 End 会失效
- 〔做法第 5 步〕hitTestBehavior(value: HitTestMode): T 未设时为 HitTestMode.Default：自身及子节点响应触摸测试，但阻塞兄弟节点的触摸测试；Transparent 自身和子节点响应且不阻塞兄弟和祖先；None 自身不响应、不阻塞子节点和兄弟。Stack 中多个节点触摸区域重叠、最上层节点的子组件命中时，默认只对最上层节点做触摸测试，只有给最上层节点设 HitTestMode.Transparent，下层节点才参与触摸测试
- 〔做法第 5 步〕ArkUI Stack 中叠在 Scroll 内容之上、宽高都为 100% 的 Column（未设 hitTestBehavior）在设备上挡住下层轮播和页面的滑动
- 〔原因 / 做法第 2、5 步〕ArkUI Stack 的子组件写 .align(...) 在设备上不改变它在 Stack 里的位置，仍按父 Stack 的 alignContent 摆放：alignContent 为 TopStart 的 Stack 里写 .align(Alignment.End) 的滚动条容器停在 Stack 左缘（控件树 dump）；alignContent 为 Center 的标题栏 Stack 里写 .align(Alignment.Start) 的返回图标仍在中央、压在标题上；未设 alignContent 的 Stack 里写 .align(Alignment.Top)、.align(Alignment.Bottom) 的顶栏和底栏都居中，底栏显示在页面中间
- 〔做法第 2 步〕ArkTS 里写 Alignment.CenterEnd、Alignment.CenterStart 编译报错（不是 ArkUI Alignment 的成员）
- 〔做法第 6 步〕Stack 的子组件按声明顺序入栈，后声明的渲染层级更高、覆盖前面的；zIndex(value: number): T 改变同一容器内兄弟组件的显示层级，值大的在上，不能跨容器改层级，zIndex 相等时按声明顺序（后声明的在上）
- 〔做法第 7 步〕layoutWeight(value: number | string): T 只在 Row、Column、Flex 中生效，默认 0：父容器尺寸确定时，没设 layoutWeight（或为 0）的子组件先占位，设了大于 0 的子组件从主轴剩余空间按权重分配，分配时忽略子组件自身的 width/height，保留 minWidth/minHeight 约束
- 〔做法第 7 步〕alignRules(value: AlignRuleOption): T（API 9 起）与 alignRules(alignRule: LocalizedAlignRuleOptions): T（API 12 起，水平方向用 start、end）只在父容器是 RelativeContainer 时生效；AlignRuleOption 的 left、right、middle 取 { anchor, align: HorizontalAlign }，top、bottom、center 取 { anchor, align: VerticalAlign }（API 23 起类型名为 HorizontalAlignParam、VerticalAlignParam）；父容器 RelativeContainer 的标识默认是 '__container__'，被引用为锚点的兄弟组件要用 id 属性设标识
- 〔做法第 7 步〕RelativeContainer 中子组件的 margin 指子组件到该方向锚点的距离，alignRules 没设某个方向的锚点时该方向的 margin 不生效；RelativeContainer 不设 width、height 时布局表现与设为 100% 相同

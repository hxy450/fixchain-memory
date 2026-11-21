# 由内容定尺寸的父级（列表行、wrap_content 头部、FIT_CONTENT 半模态）里不写 width/height('100%')：描边背景画在节点自身，行内撑满用 Stretch；源端描边不改尺寸时注意 .border() 计入测量（定尺寸遮罩中的居中弹卡不在此列，宽度按源窗口规则）

## 何时使用

界面实现与规格映射阶段，翻译用 fillMaxSize()、matchContentSize 贴合内容的选中指示器、描边或背景，为高度由内容决定的行加铺满的背景层（滑删进度背景等），或把 Compose Modifier.border 这类只绘制、不改测量的修饰符落到 ArkUI 容器上时；把 match_parent 高度翻译到 ListItem、列表行组件、折叠头部背景层或 bindSheet 内容根时；转换将被宿主嵌入的子组件（Fragment 转子组件）、确定根节点及各状态视图的高度约束时；为 GridView/ListView 条目补高度、好让子层撑满时

## 适用情境

源端指示器或背景层以 fillMaxSize、matchContentSize 贴合某个由内容定尺寸的格子；目标准备在 Stack/Row 里叠一层 width/height('100%') 的节点来画描边或背景。也包括列表行里的 Stack 没有确定高度，准备放一层宽高 100% 的背景子节点；或源 border 画在调用方已定尺寸的盒内侧，目标容器自身不设宽高、尺寸由槽内容决定。也包括源 match_parent 子视图位于 wrap_content 的行、AppBar 或 BottomSheet 容器中，实际随内容或兄弟高度；目标放进 List、ListItem、Scroll 或 FIT_CONTENT 半模态，准备直译为 height('100%')。也包括被宿主嵌入的子组件：源布局根节点与空态容器都是 wrap_content，在宿主 NestedScrollView 的 wrap_content 槽位里按内容取高；目标根 Column 与 loading/empty/error 各分支写 height('100%')，宿主把它放进 Scroll 内未设高度的 Column。 也包括 GridView/ListView 条目由内容定高，目标准备用 width('100%') 加 aspectRatio 或固定 vp 给条目定高，好让子层写 100%。 也包括 wrap_content 宽的 PopupWindow 内容是竖向 LinearLayout：一个定宽子项（如取色器）与若干 match_parent 的滑杆或自定义 View 并列，目标要为弹层与滑杆写出数值宽度。

## 例外与边界

- 父节点有确定的宽高（显式数值，或已被外层约束定死）时，百分比层按该尺寸解析，可以使用；为满足这一条而给行或格子补的高度取源端该项的实际测量结果，不用 aspectRatio、固定 vp 或 layoutWeight 凑
- 页面根 Stack 等定尺寸遮罩里的居中弹窗卡片：父级已定尺寸，宽度按源端窗口规则写（Holo、Material 系与 AppCompat 的 AlertDialog 默认窗口宽 wrap_content，最小宽取当前屏宽的竖屏 95%、横屏 65%（large 屏 80%/55%，xlarge 屏 72%/45%），内容更宽时随内容；可见卡片再减去窗口背景的左右内缩：Material 与 AppCompat 各 16dp，Holo 各 8dp），不适用本条，也不从本条取固定 vp 估值

## 原因

ArkUI 的百分比尺寸在由内容定尺寸的父级里会向上取到最近的确定尺寸，把格子撑大（工程迁移陷阱表与设备实测一致）。来源中选中格内的 height('100%') 描边层解析到被撑高的 Tab 行高度，选中格变成约 299×597vp；与横向 Scroll 未定高叠加后，首帧只看得到前两项。列表行里的 100% 背景层同样会按更大的约束铺开，把行撑到整屏高。另一方面，在没有显式宽高的容器上写 .border()，来源 dump 显示描边计入了容器测量，盒子比内容大出描边宽度、后续卡片随之错位；Compose 的 Modifier.border 只在已定尺寸的盒内绘制，不改尺寸。源 match_parent 直译成 height('100%') 时，单行或折叠头部会撑满整个 List 视口，半模态内容根会把 FIT_CONTENT 弹层撑到上限。被嵌子组件根节点的 '100%' 在 Scroll 的无界父链里会解析成视口高度，把首屏后续区块挤出。 为了让 100% 子层有确定父尺寸而用宽高比或经验值给行补高度，行高会与源端测量不符。

## 做法

1. 描边、背景直接写在内容节点上（.border()、.backgroundColor()、.borderRadius()），描边与内容的间距用 padding 表达；源端描边相对内容有内缩时，把内缩量拆到外层与内容节点的 padding 里。
2. 选中与未选中两态保留同样宽度的描边，未选中用 Color.Transparent，切换时尺寸不变。
3. 写完 grep width('100%') 与 height('100%')，逐处确认父级有确定尺寸。 需要给行或格子补高度时按源端该行的测量取值：源条目在 GridView/ListView 里时，行高＝条目内容按 UNSPECIFIED 测得的高（wrap_content 图片为密度放大后的固有高）加条目 padding，写在 GridItem/ListItem 上；去 Adapter.getView 的 setLayoutParams 与 padding、条目布局 XML 的 layout_height、内含图片的密度目录与像素尺寸里查。
4. 行或卡片的铺满背景改用 .background(builder) 画在容器自身，或用列表项自带的滑动操作（ListItem.swipeAction）。
5. 源端描边只绘制、不改尺寸时，先写明目标盒尺寸由谁决定：能拿到调用方尺寸就把宽高提升到带描边的节点上；尺寸只能由内容决定时，改用按 onSizeChange 回读的数值宽高叠一层 position({ x: 0, y: 0 }) + hitTestBehavior(HitTestMode.None) 的描边层（首帧会缺描边），规格验收写明“描边不改变盒尺寸”。
6. 行内交叉轴撑满（如行首竖条、拖拽柄随行高）用 alignSelf(ItemAlign.Stretch) 或明确尺寸；头部背景或遮罩层按源可见区域给显式高度（如工具栏高加头部块），或把背景画在容器自身。源 LinearLayout（含 wrap_content 的 PopupWindow 内容）在交叉轴（竖向的宽、横向的高）为 wrap_content 时，该轴尺寸只由非 match_parent 子项决定（竖向 LinearLayout 取这些子项的最大宽加各自 margin，match_parent 子项只计 margin，再加父 padding，且不小于 minWidth；子项全是 match_parent 时才取它们测得的最大宽），match_parent 子项随后按该尺寸以 EXACTLY 重测；主轴方向不按此算，match_parent 子项照常计入总长度；需要算出数值（弹层宽、自绘子项的测量宽）时按这个顺序，不让 match_parent 子项的偏好尺寸参与父级定宽，自定义 View 的偏好长度只在 AT_MOST/UNSPECIFIED 下生效（指覆写了 onMeasure、按 resolveSize 一类方式取偏好的 View；没覆写 onMeasure 的 View 走 getDefaultSize，AT_MOST 下直接取父给的上限）。
7. 半模态内容根的 Scroll/Column 不写 height('100%')，由弹层上限约束高度；不写 100% 不等于能滚动：内容 Scroll 还要设非 None 的 edgeEffect，才能在 FIT_CONTENT 弹层里超高后拖动（见 lesson-df1f691759f84ba9e688 第 3 步）。
8. 被嵌子组件按源布局根节点与各状态容器的 layout_height 映射：wrap_content 不写 height('100%')，空态居中用内容高度或 constraintSize 最小高度；宿主向无高度槽位嵌入组件前，读被嵌组件 build() 根与各状态分支的高度修饰，有百分比高度就先改组件或在槽位按源端尺寸给显式高度，再核对首屏后续区块仍可见。

## 可选检查

- 源端描边不改尺寸而有疑问时，用 dumpLayout 核对带描边容器的 bounds 与内容子项一致。
- 行或头部出现整屏高、或弹层被撑到上限时，检索该子树中的 '100%' 高度并确认其父级是否定高

来源支持：13 张卡 · 已知 8 次迁移（部分未记录） · 已知 7 个应用（部分未记录）

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；实现对照 OpenHarmony arkui_ace_engine 标签 OpenHarmony-v6.0-Release；安卓 Android SDK 源码 android-36.1；Android SDK 平台资源 android-30、android-36、android-37.0；appcompat 1.1.0、1.8.0；androidx.compose.foundation:foundation 1.0.0、foundation-android 1.12.0；foundation-layout 1.0.0、foundation-layout-android 1.12.0（均为 Maven 源码包）。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因〕ArkUI 组件的 width/height 用百分比时，按最近一个设了固定尺寸的祖先节点的尺寸计算，不按直接父节点由内容撑出的尺寸；所以在不定尺寸的父级里写 '100%'，取到的是更上层定了尺寸的节点的宽高。〔成立范围：依据是尺寸设置文档的说明。对 width、height 的百分比成立。不成立：直接父节点自身设了数值宽高，或已被外层约束定死时，百分比按直接父节点解析；bindSheet 用 SheetSize.FIT_CONTENT 时文档另写明 builder 根节点高度不能用百分比（弹层高度反过来依赖内容）。〕
- 〔做法第 5 步〕ArkUI 的 .border() 边框宽度和 padding 一样计入布局：不设宽高时盒子尺寸是内容加 padding 加边框宽度，设了宽高时边框占用盒内空间、内容区相应缩小；.outline() 外描边画在组件外侧，不影响布局，也不占组件尺寸。〔成立范围：依据：OpenHarmony arkui_ace_engine 标签 OpenHarmony-v6.0-Release 的 LayoutProperty::CreatePaddingAndBorder（布局把 padding 与 borderWidth 合并处理）与 Flex 布局算法（Row/Column 定了交叉轴尺寸时内容区 = 尺寸 − padding − 边框）；outline 依据是外描边文档说明。不成立：个别组件的 pattern 声明边框不占位（实现中 BorderUnoccupied 返回 true）时边框不计入。〕
- 〔适用情境〕Compose 的 Modifier.border 只是绘制修饰，不改变被修饰元素的测量尺寸（1.0.0 为 composed 加 drawWithCache，1.12.0 的 BorderModifierNode 是 DelegatingNode 加 SemanticsModifierNode，不是布局节点）；BoxScope.matchParentSize() 的子项不参与决定 Box 尺寸，等其余子项定出 Box 尺寸后按该尺寸测量，而 fillMaxSize() 会参与，让 Box 撑满可用空间。〔成立范围：androidx.compose.foundation 与 foundation-layout 1.0.0、1.12.0 源码一致。matchParentSize 是 BoxScope 的扩展，只对 Box 的直接子项有效。不成立：border 写在已用 size/padding 定尺寸的盒子上时尺寸由那些修饰决定，与 border 无关；Box 外的 fillMaxSize 按所在父级约束取最大值，父级在某轴的约束无界（如 verticalScroll 内的高度）时该轴不撑满。〕
- 〔做法第 6 步〕LinearLayout 交叉轴（竖向时的宽、横向时的高）的 MeasureSpec 不是 EXACTLY 时，该轴尺寸取非 match_parent 子项测得的最大值（各含 margin），match_parent 子项只贡献 margin，再加父 padding、不小于最小建议尺寸，最后不超过父给的 AT_MOST 上限；只有子项全为 match_parent 时才取它们测得的最大值；随后 match_parent 子项按算出的尺寸以 EXACTLY 重测。主轴方向的 match_parent 子项照常测量并计入总长度（父的主轴为 AT_MOST 或 EXACTLY 时按剩余空间测）。〔成立范围：android-36.1 源码；GONE 子项不参与。不成立：父级给的交叉轴是 EXACTLY（layout 写了数值，或 match_parent 且父级已定尺寸）时直接用父给的尺寸；带 layout_weight 的子项另有重测流程。〕
- 〔做法第 3 步〕ListView、GridView 测量条目时，条目 LayoutParams 的高为正数才以 EXACTLY 测，match_parent 与 wrap_content 都按 UNSPECIFIED 测，即条目高只由内容决定；Adapter.getView 里用 inflate(layout, null) 时根节点的 layout_height 不会进入 LayoutParams，列表改用默认的 MATCH_PARENT 宽、WRAP_CONTENT 高。〔成立范围：android-36.1 源码；只对 AbsListView 系（ListView、GridView）成立。不成立：inflate(layout, parent, false) 时 XML 根节点的 layout_height 生效；getView 里 setLayoutParams 设了数值高时按该值 EXACTLY；RecyclerView 由 LayoutManager.getChildMeasureSpec 决定，不在此列。〕
- 〔做法第 6 步〕alignSelf 只对 Row、Column、Flex、DynamicLayout 的直接子组件和 GridRow 中的 GridCol 生效，父容器是 Stack、ListItem、RelativeContainer 等其他容器时写了不起作用；ItemAlign.Stretch 在 Row/Column 中不论子组件是否设了交叉轴尺寸都拉伸到容器的交叉轴尺寸，Flex 设了换行时拉伸到当前行最长的那个。〔成立范围：依据是 Flex 布局属性文档与 ItemAlign 文档说明。容器未设交叉轴尺寸时，被拉伸到的尺寸由子组件测量结果决定（OpenHarmony arkui_ace_engine 标签 OpenHarmony-v6.0-Release 的 Flex 布局算法取子组件交叉轴尺寸的最大值），所以未定高的 Row 里被拉伸的子项随最高的子项走。不成立：容器设了交叉轴尺寸时按该尺寸减 padding 拉伸。〕

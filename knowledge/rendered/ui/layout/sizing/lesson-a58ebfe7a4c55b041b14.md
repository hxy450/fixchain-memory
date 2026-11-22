# 由内容定尺寸的父级（列表行、wrap_content 头部、FIT_CONTENT 半模态）里不写 width/height('100%')：描边背景画在节点自身，行内撑满用 Stretch；源端描边不改尺寸时注意 .border() 计入测量（定尺寸遮罩中的居中弹卡不在此列，宽度按源窗口规则）

## 何时使用

界面实现与规格映射阶段，翻译用 fillMaxSize()、matchContentSize 贴合内容的选中指示器、描边或背景，为高度由内容决定的行加铺满的背景层（滑删进度背景等），或把 Compose Modifier.border 这类只绘制、不改测量的修饰符落到 ArkUI 容器上时；把 match_parent 高度翻译到 ListItem、列表行组件、折叠头部背景层或 bindSheet 内容根时；转换将被宿主嵌入的子组件（Fragment 转子组件）、确定根节点及各状态视图的高度约束时；为 GridView/ListView 条目补高度、好让子层撑满时

## 适用情境

源端指示器或背景层以 fillMaxSize、matchContentSize 贴合某个由内容定尺寸的格子；目标准备在 Stack/Row 里叠一层 width/height('100%') 的节点来画描边或背景。也包括列表行里的 Stack 没有确定高度，准备放一层宽高 100% 的背景子节点；或源 border 画在调用方已定尺寸的盒内侧，目标容器自身不设宽高、尺寸由槽内容决定。也包括源 match_parent 子视图位于 wrap_content 的行、AppBar 或 BottomSheet 容器中，实际随内容或兄弟高度；目标放进 List、ListItem、Scroll 或 FIT_CONTENT 半模态，准备直译为 height('100%')。也包括被宿主嵌入的子组件：源布局根节点与空态容器都是 wrap_content，在宿主 NestedScrollView 的 wrap_content 槽位里按内容取高；目标根 Column 与 loading/empty/error 各分支写 height('100%')，宿主把它放进 Scroll 内未设高度的 Column。 也包括 GridView/ListView 条目由内容定高，目标准备用 width('100%') 加 aspectRatio 或固定 vp 给条目定高，好让子层写 100%。 也包括 wrap_content 宽的 PopupWindow 内容是竖向 LinearLayout：一个定宽子项（如取色器）与若干 match_parent 的滑杆或自定义 View 并列，目标要为弹层与滑杆写出数值宽度。

## 例外与边界

- 父节点有确定的宽高（显式数值，或已被外层约束定死）时，百分比层按该尺寸解析，可以使用；为满足这一条而给行或格子补的高度取源端该项的实际测量结果，不用 aspectRatio、固定 vp 或 layoutWeight 凑
- 目标写的是 LayoutPolicy.matchParent（不是 '100%'），且父容器设了 LayoutPolicy.wrapContent（API 20 起）时，容器先由其它确定尺寸的子组件撑开、matchParent 子组件再匹配容器，与源端 wrap_content 父级里 match_parent 子项的结果一致，不按本条改写；父容器里没有确定尺寸的子组件时两者都为 0，仍按本条处理
- 页面根 Stack 等定尺寸遮罩里的居中弹窗卡片：父级已定尺寸，宽度按源端窗口规则写（Holo、Material 系与 AppCompat 的 AlertDialog 默认窗口宽 wrap_content，最小宽取当前屏宽的竖屏 95%、横屏 65%（large 屏 80%/55%，xlarge 屏 72%/45%），内容更宽时随内容；可见卡片再减去窗口背景的左右内缩：Material 与 AppCompat 各 16dp，Holo 各 8dp），不适用本条，也不从本条取固定 vp 估值
- 第 4 步把铺满层挪进 .background(builder) 只适用于纯展示的层：自定义背景不响应事件，内容更新也不一定跟着重绘（文档写 API 20 起才支持动态更新）；层要响应点击、手势，或随滑动进度等状态变化时，改用 ListItem.swipeAction，或保留独立节点并按源端测量给显式尺寸

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

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的平台资源与源码；androidx.appcompat:appcompat 1.7.1（包内资源）；androidx.core:core 1.13.0、androidx.compose.foundation:foundation-android 1.10.4（字节码）。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 3 步〕ArkUI 组件尺寸用百分比时，以最近一个设置了固定大小的祖先节点的尺寸为参照计算；父级自身没设宽高、尺寸随内容时，它不是这个参照
- 〔原因〕设备上横向 Scroll（写 height('auto')）里的 Row 由文字定高，选中格 Stack 里叠一层 width('100%').height('100%') 的指示层时，选中格量得约 299×597vp、整个 Tab 行 356×597vp，首帧只看得到前两项；height('auto') 对 Scroll 不起定高作用
- 〔原因〕设备上 List 行里没有确定高度的 Stack 放一层 width/height('100%') 的背景 Row 时，ListItem 和背景 Row 都量得 581vp，只剩首行可见；高度自适应的 Row 里写 height('100%') 的子项取的是父级最大约束，不是行内最高兄弟项的高度
- 〔原因 / 做法第 8 步〕设备上子组件根 Column 及各状态分支写 height('100%')、被放进 Scroll 内没设高度的 Column 时，'100%' 解析成视口高度，空态卡几乎占满内容区，其后的区块被挤出首屏
- 〔做法第 7 步〕bindSheet 的 SheetOptions.height 默认 LARGE；SheetSize.FIT_CONTENT 让半模态容器高度去适应 builder 根节点的布局，此时 builder 根节点的高度不能用百分比（两者不能互相依赖）；底部弹窗竖屏时最大高度到距状态栏 8vp 处
- 〔做法第 7 步〕Scroll 没设 edgeEffect 时取 EdgeEffect.None（滑到边缘无效果）；options.alwaysEnabled 决定内容小于组件自身时是否仍开启边缘效果
- 〔做法第 7 步〕设备上 bindSheet(height: SheetSize.FIT_CONTENT) 的内容 Scroll{Column} 没设 edgeEffect 时，内容超过弹层上限后在弹层里拖不动；其他高度档和非半模态里的 Scroll 卡里没有测
- 〔原因 / 做法第 5 步〕ArkUI 布局元素：组件区域就是 width/height 设的大小，组件内容区为组件区域减去 border，内容区是子组件测算时的限制；设了固定宽高时内容大小为宽高减去 padding 和 border，所以没设宽高、由内容撑开的容器，区域等于内容加 padding 加 border
- 〔原因 / 做法第 5 步〕设备上没写 width/height 的 Stack 加每边 1vp 的 .border() 时，量得 Stack 172×250、其中内容 Column 170×249（源端同一卡片 170×250），后续卡片的左沿随之右移约 2vp
- 〔原因 / 做法第 5 步〕Compose 的 Modifier.border 生成的 BorderModifierNode 只委托一个绘制节点（CacheDrawModifierNode），没有布局节点，不参与测量，描边画在前面修饰符已定的尺寸里
- 〔做法第 5 步〕onSizeChange 只在布局变化导致组件尺寸改变时触发，是布局过程中的同步回调；回调给的尺寸因计算精度可能与物理尺寸略有差异；在回调里直接改状态变量，可能被并进同时进行的动画
- 〔做法第 5 步〕position 在组件尺寸测量完成后才作用；父组件是 Row、Column、Flex 时设了 position 的子组件不占位（全部子组件都设了时父组件按 0×0 测算）；Position 类型以父组件内容区左上角为原点；文档另写：父组件没设固定宽高时，按第一个设了固定宽高的祖先做绝对定位；卡里在没设宽高的容器里叠 position({ x: 0, y: 0 }) 的描边层，设备上量得描边层与容器对齐
- 〔做法第 5 步〕设备上用 .overlay() 承载遮罩层时，层里的 '100%' 不按宿主尺寸解析（约 136vp 对 60vp 的行），而且遮罩层吞掉了内容的横向滑动
- 〔做法第 6 步〕alignSelf 覆盖父容器的 alignItems，只在 Flex（FlexWrap.NoWrap 时）、Column、Row、DynamicLayout、GridRow 里生效；ItemAlign.Stretch 在不换行的情况下无论子项这一轴是否设了尺寸都拉伸到容器的交叉轴尺寸，换行的 Flex 里拉到当前行最长元素的尺寸
- 〔做法第 6 步〕LayoutPolicy.matchParent（API 15 起；API 15–19 只有 Row、Column 的宽高支持，API 20 起所有基础组件支持）让组件等于父组件内容区（不含 padding、border）；容器设 wrapContent（API 20 起）且子组件设 matchParent 时，容器先由确定大小的子组件撑开，matchParent 子组件再匹配容器，没有确定大小的子组件时两者都为 0；只在交叉轴设 matchParent 的子组件，API 26 起才参与 Row、Column、Flex 主轴的自适应测量（超出本机 SDK 的 API 23）
- 〔做法第 4 步〕background(CustomBuilder) 的自定义背景渲染有延迟、不能响应事件、不支持嵌套；它叠在 backgroundColor、backgroundImage 之上（content 为 ResourceColor 或设了 ignoresLayoutSafeAreaEdges 时才在最底层）；content 为 CustomBuilder 时背景不跟随 builder 内容更新而变化（文档另写 API 20 起支持动态更新背景）
- 〔适用情境 / 做法第 6 步〕安卓 LinearLayout 竖向测量时宽不是 EXACTLY：lp.width 为 MATCH_PARENT 的子项在 alternativeMaxWidth 里只计 margin，只要不是全部子项都 MATCH_PARENT，容器宽取 alternativeMaxWidth 加左右 padding、再与最小宽取大；定宽后 forceUniformWidth 以测得宽、EXACTLY 重量这些子项；横向测量的高（alternativeMaxHeight、forceUniformHeight）同理
- 〔做法第 6 步〕安卓 View.getDefaultSize（没覆写 onMeasure 的 View 走它）在 AT_MOST、EXACTLY 下都直接取父给的尺寸，UNSPECIFIED 下取建议最小尺寸；resolveSizeAndState 在 AT_MOST 下取期望尺寸与上限中较小者（超出时带 MEASURED_STATE_TOO_SMALL），EXACTLY 下取父给的尺寸
- 〔适用情境 / 原因〕安卓 ScrollView 在没设 fillViewport 时以 UNSPECIFIED 测子 View 的高，androidx.core 的 NestedScrollView 同样以 UNSPECIFIED 测子高，所以滚动容器里写 match_parent 的子 View 实际按内容取高
- 〔做法第 3 步〕安卓 GridView 的条目没有另设 LayoutParams 时取 AbsListView.LayoutParams(MATCH_PARENT, WRAP_CONTENT)；条目按列宽 EXACTLY 测宽、按 getChildMeasureSpec(UNSPECIFIED, 0, lp.height) 测高，WRAP_CONTENT 时即 UNSPECIFIED
- 〔做法第 3 步〕安卓位图按密度换算尺寸时取 (尺寸×目标密度 + 源密度/2) / 源密度 的整除结果；drawable-ldpi 的源密度是 120，所以 ldpi 下 N 像素的图在密度 D 的设备上固有尺寸为 (N×D + 60) / 120 取整
- 〔做法第 6 步〕应用和 Activity 主题没有另设 actionBarSize 时：平台 Theme.Material 取 action_bar_default_height_material，默认 56dp、values-land 48dp、values-sw600dp 64dp；AppCompat 1.7.1 主题取 abc_action_bar_default_height_material，同样是默认 56dp、横屏 48dp、sw600dp 64dp
- 〔例外与边界〕平台 AlertDialog 主题（Theme.Material.Dialog.BaseAlert、Theme.Holo.Dialog.BaseAlert）在应用没有另设时 windowMinWidthMajor/Minor 取 dialog_min_width_major/minor：默认 65%/95%，values-large 55%/80%，values-xlarge 45%/72%；DecorView 竖屏取 Minor、横屏取 Major；浮动窗口布局为 WRAP_CONTENT；Material 对话框背景 dialog_background_material 四边各内缩 16dp；Holo 的 dialog_full_holo_dark 九宫格在 mdpi 下外圈 8px 是渐变阴影，其内才不透明
- 〔例外与边界〕AppCompat 1.7.1 的对话框主题在应用没有另设时 windowMinWidthMajor/Minor 取 abc_dialog_min_width_major/minor：默认 65%/95%，values-large 55%/80%，values-xlarge 45%/72%；API 21 起的 abc_dialog_material_background 四边各内缩 16dp，dialogCornerRadius 为 2dp

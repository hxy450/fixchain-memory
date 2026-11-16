# RecyclerView 的列表和网格

agent 会看到什么：读到 RecyclerView 及其多类型 Adapter（addItemType、onCreateViewHolder）、GridLayoutManager / SpanSizeLookup、ItemDecoration、ItemTouchHelper；产物里 List / Grid 的区块内容、通栏和跨度、项间距和滑动操作

## 规矩

- rule-5ca3358dd2c8｜页面主体是 RecyclerView 多类型 Adapter 时，逐个读 item 布局再实现区块，不凭标题推断｜读到：页面布局只有 RecyclerView（常在 SwipeRefreshLayout 里）外壳，Adapter 用 addItemType 或 onCreateViewHolder 按类型 inflate 多个 item 布局，各区块的内容在绑定方法里填；写错：目标区块只剩标题文字：Grid 绑空数组、横向 List 固定高度没有内容、趋势图写成纯文本列表，像占位卡片
- rule-778d28683bb0｜源多列网格里通栏的广告位在目标恒为空时，Grid 不为它生成 GridItem，ForEach 只渲染内容项｜读到：源端 GridLayoutManager 多列，SpanSizeLookup.getSpanSize 对广告或占位项返回满列数，广告在数据层按固定间隔插入；派工或规格把广告定为 no-op 空容器；写错：目标 Grid 的 ForEach 仍为恒空广告位生成 GridItem（零高 Row 或空组件），并用 columnStart/columnEnd、GridLayoutOptions 的 irregularIndexes / onGetIrregularSizeByIndex 让它通栏，注释称零高塌陷与 Android 一致
- rule-d12b5b5c3410｜网格里不同跨度的卡片要同行等高时，按实际列宽推导宽卡 aspectRatio，不套组件原生宽高比｜读到：源列表用 12 列网格按卡片规格分配 spanCount（窄卡占 4、宽卡占 8），常量里有组件自身内容尺寸（如宽卡 334.75 × 158）；参考截图里同一行的窄卡和宽卡外框等高；写错：宽卡外框写成 .aspectRatio(原生宽 / 原生高)，套在百分比列宽且两侧有固定内边距的单元上，宽卡比同行窄卡矮
- rule-98f656c81720｜ItemDecoration 的项偏移落到容器 padding 或 Grid gap，不转成外 margin｜读到：RecyclerView 挂了 ItemDecoration，getItemOffsets 给每项的 outRect 设偏移；RecyclerView 自身没有 layout_margin；写错：目标 Grid 或 List 的链上写了 .margin(N) 作外边距，并配 .width('100%')
- rule-8d726695dac0｜滑动操作转 swipeAction 时挂在 ListItem 上，不挂在 @Builder 行的根组件上｜读到：源端用 ItemTouchHelper 或滑动操作类给 RecyclerView 行加滑动按钮，规格和映射写「→ ListItem.swipeAction」；写错：.swipeAction(...) 接在行内容 @Builder 根 Row 的属性链末尾，LazyForEach / ForEach 里的 ListItem 只调用 this.行Builder(item)
- rule-4eea53c71337｜源端评价图片最多 9 张、3 列九宫格时，目标用 Grid 三列并截取前 9 张｜写错：目标条目图片写成 `Row` + `Repeat` 固定尺寸横排，没有张数上限和列数，而源端是九宫格
- rule-b315471a659c｜ItemTouchHelper 左右滑删除用 PanGesture 跟手加阈值和回弹，不用 SwipeGesture｜读到：源 `ItemTouchHelper`（`SimpleCallback` 左右滑，`onSwiped` 里删除）；写错：`ListItem` 上挂 `SwipeGesture({ direction: SwipeDirection.Horizontal }).onAction(...)`，识别即删除：没有跟手位移、半宽或甩动阈值、回弹

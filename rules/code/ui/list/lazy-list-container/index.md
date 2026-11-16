# LazyColumn、LazyRow 和 RecyclerView 列表容器

agent 会看到什么：读到 Compose 的 LazyColumn / LazyRow（contentPadding、horizontalArrangement、verticalArrangement）或 RecyclerView 纵向列表，产物里是 List、Scroll 包 Column / Row 的容器写法

## 规矩

- rule-8efb6be82f3b｜从顶部排的可变长度纵向列表用 List；Scroll 包 Column 时设 .align(TopStart)｜读到：Compose LazyColumn(Modifier.fillMaxSize(), verticalArrangement = Arrangement.spacedBy(...)) 从顶部排列，项数可能不足一屏；写错：写成 Scroll() { Column() { ForEach(...) }.width('100%') }.layoutWeight(1)，Scroll 没设 .align，Column 也没撑满高度
- rule-495d3c403988｜横向列表的 contentPadding 写成 contentStart/EndOffset，不写 padding｜读到：Compose 的 LazyRow(contentPadding = PaddingValues(start = …, end = …))；写错：对应的横向 List（listDirection(Axis.Horizontal)）写成 .padding({ left/start: …, right/end: … })，项滚到内距处被裁切
- rule-512034424c34｜LazyRow(SpaceEvenly) 写成横向 Scroll 包 minWidth 100% 的 Row，槽位恒在｜读到：LazyRow(horizontalArrangement = Arrangement.SpaceEvenly) 里放固定几个 item，item 内用 AnimatedVisibility 控制显隐；写错：写成 Row().width('100%').justifyContent(FlexAlign.SpaceEvenly)，子项用 if 增删，外面没有 Scroll

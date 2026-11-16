# LazyColumn 的 stickyHeader 吸顶

agent 会看到什么：读到 Compose LazyColumn 里的 stickyHeader { … }（或按开关在 stickyHeader 和 item 之间切换），外层折叠顶栏有「内容未满不折叠」一类判断；产物里吸顶内容挪到 List 外做固定兄弟、List 没有 .sticky(StickyStyle.Header)，或决定折叠的高度测量没把 ListItemGroup 的 header 算进去

## 规矩

- rule-6ed977a1b4b9｜stickyHeader 写成 ListItemGroup header 加 sticky，不移出 List｜读到：Compose LazyColumn 里有 stickyHeader { … }，或按开关在 stickyHeader 与 item 之间切换同一块内容；写错：吸顶内容被放到 List 外做固定兄弟（先放吸顶内容、再放只含其余项的 List），注释或报告称「Stack+offset」「行为等价」；或 List 上没有 .sticky(StickyStyle.Header)
- rule-02cb6b0590a4｜吸顶分支里判断内容是否超出视口时，测量挂在 ListItemGroup 上把头部一起算｜读到：源端 LazyColumn 带 stickyHeader，外层折叠顶栏有「内容未满不折叠」一类判断（如 enabledWhenBodyUnfilled = false）；写错：吸顶分支里决定是否折叠的内容高度测量只挂在 ListItem 里的 Column 上，没把 ListItemGroup 的 header 算进去

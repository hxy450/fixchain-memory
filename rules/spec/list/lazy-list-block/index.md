# Compose 惰性列表（LazyColumn / LazyRow）区块

agent 会看到什么：读到 Compose 页面里的 LazyColumn / LazyRow 列表区块（可能在另一文件的子 Composable 里，带分区、空态、加载态）；交回的规格里这块只有一行组件映射，或少了状态分支和滚动方向

## 规矩

- rule-685f4002f8d3｜页面把列表区块交给另一文件的子 Composable 时，规格要打开正文写出各条件分支｜读到：页面 Composable 把整块区域交给另一个文件里的子 Composable（带参数调用一次），子组件里是按类型分区的 LazyColumn；写错：规格里这块只有一行“LazyColumn → List + ListItem + LazyForEach”，没写空列表、加载中、分区标题、扫描开关等分支，也没标 UNCLEAR
- rule-6b25c53a0ef4｜规格每页列出空态和加载态清单，写明源位置、字符串 key 和图标，并留在完成摘要里｜读到：源页面或其子组件有列表为空、加载中时的内联状态（图标 + 标题 + 提示）；写错：页规格没有空态/加载态清单，或完成摘要里列了各 UI 区块却没有空态条目
- rule-a2686bf2e144｜源是 LazyRow/LazyColumn 时，规格映射写带方向的可滚动容器和恒在槽位，不写成普通 Row｜读到：Compose 源码里有 LazyRow / LazyColumn，item 个数固定、item 内用 AnimatedVisibility 控制显隐；写错：规格映射表写成「LazyRow → Row + …」这类普通 Row / Column，没写滚动方向、排列方式，也没写 item 是否恒在
- rule-56a8eeda878a｜规格给吸顶列映射时写明吸顶内容仍属滚动容器，只给 ListItemGroup header 加 sticky｜读到：源端 Compose LazyColumn 里有 stickyHeader，或按开关在 stickyHeader 与 item 间切换；写错：规格的吸顶映射并列「Stack + offset」这类可能把头部移出滚动容器的方案，或没写必须保持的行为（从吸顶区起拖照常滚动）；验收条目里没有从吸顶区起拖的检查

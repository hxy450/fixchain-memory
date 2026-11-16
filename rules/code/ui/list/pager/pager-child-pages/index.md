# ViewPager / Tab 承载的子 Fragment 页

agent 会看到什么：读到 TabLayout / ViewPager 配了子 Fragment 列表；产物里 Tabs、Swiper 子页的内容和列表项、@Builder 槽位的参数、子页拿的导航栈，以及决定建几个子页的解析结果

## 规矩

- rule-cb5d7fd51a08｜源布局用 ViewPager 承载子 Fragment 的列表时，先读子 Fragment 和 item 布局再写｜读到：页面 XML 有 TabLayout + ViewPager，页面 Fragment 代码里给 ViewPager 配了子 Fragment 列表（tab 标题一组、子 Fragment 一组）；写错：目标端对应子页的 List / ListItem 是按截图或猜测写的；读过的文件里没有子 Fragment 的布局 XML 和 RecyclerView 的 item 布局，列表项的字段、分组和源端不符
- rule-07def1a25c26｜@Builder 槽位要显示异步加载或 @Trace 会变的数据时，不作位置值参，槽体内直读 this 上的状态｜读到：源端宿主 Fragment 用 Tab / ViewPager 嵌子 Fragment，子 Fragment 显示异步加载的列表和选中位置；写错：@Builder 槽位声明成多个位置值参（数组、选中索引、回调），调用处传入 @ObservedV2 / @Trace 状态对象上的属性值（如 this.state.list、this.state.selectedIndex）；槽体只有 FWD-REF 占位时也是这个签名
- rule-a1a20e11354c｜Tab 或 Swiper 承载的子页只用 @Consumer 注入的根栈，onReady 不改写栈｜读到：源端 Fragment 由 ViewPager 或底部 Tab 承载；规格标「页面类型 fragment（Tab 判定）」，父页的 Swiper / Tabs 预留了这个 Tab 槽位；写错：子页声明 @Consumer('navPathStack') navPathStack 的同时，在 .onReady((context) => { this.navPathStack = context.pathStack }) 里覆盖它
- rule-3826bdcf8947｜决定页面是否创建的解析结果，区分服务端返回空和取值路径未命中，并用样例验证非空｜读到：源端拿解析出的分类列表决定建几个子页（如 Tab、二层 Swiper 的子页）；写错：取值键未命中时默默返回 `[]`，和服务端真返回空走同一分支，Tabs / Swiper 既没有子页也没有空态

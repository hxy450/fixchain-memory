# 源 Swiper 带 pagination 时，分页点叠在轮播容器内底部，不做成容器外单独一行

审的是：代码
触发（任一种）：
- 读到：源 Swiper 启用 pagination（如 pagination={{ clickable: true }}）；写错的样子：目标分页点是 Stack / Swiper 外面单独的一行 Row，或整个 Stack 改成 alignContent: Alignment.Bottom
适用范围：Web Swiper 带默认 pagination、迁成 ArkUI Swiper 加自绘分页点时
做法：
- 分页点放进轮播所在的 Stack 内、叠在 Swiper 底部，只给分页点这一层定位，不把整个 Stack 的 alignContent 改成 Bottom
- 轮播容器高度按最高一页固定，不随当前页变化
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 分页点移入轮播 Stack 叠加显示、Swiper 固定为最高一页的高度：修复后各页分页点落在同一位置；整个 Stack 改 alignContent Bottom 时出现过回归（出处：卡里修好并验证过）
针对本应用要查的：
- 分页点的默认偏移、点的尺寸和间距：源工程 node_modules 里 swiper 包的 css，按 .swiper-pagination 一类选择器找；读出 bottom、宽高、margin 换成 vp 写进分页点那一层；例：卡里查到 pagination 的 bottom 是 8px
- 最高一页的高度：源端每页的内容（标题、插图比例、边距）；逐页算出高度取最大值，写成 Swiper 的固定 height
来源：1 张卡，1 个应用
- case-acd91ce1ab3d2798a4fa（Countdate）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3、诊断；取值 1 ← 诊断

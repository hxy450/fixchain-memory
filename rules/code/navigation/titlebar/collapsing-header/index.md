# CollapsingToolbarLayout 折叠头部

agent 会看到什么：源端 AppBarLayout / CollapsingToolbarLayout 的折叠头部（match_parent 的背景图、?attr/actionBarSize、OnOffsetChangedListener 里按折叠进度给工具栏图标着色），对应目标头部的高度、滚动折叠阈值和图标两态颜色

## 规矩

- rule-aa4e36af542d｜wrap_content 头部里 match_parent 的背景层，写显式高度，不写 .height('100%')｜读到：wrap_content 的 AppBarLayout / CollapsingToolbarLayout 里放 android:layout_height="match_parent" 的背景 ImageView（高度由头部内容决定）；写错：List 首个 ListItem 里的背景 Image 或遮罩层写 .height('100%')，头部行被撑成整个 List 视口，下面的行被挤出可视区
- rule-17c17ad559a4｜代码里镜像资源数值（如工具栏高度常量）时，和资源取同一个已核定的值并注明来源主题｜读到：布局里折叠工具栏、头部 marginTop 等也用 ?attr/actionBarSize 参与计算；写错：代码里另写 `private readonly` 的 number 常量（= 56）参与折叠阈值和头部高度运算，和 float 资源各写各的，或照抄兄弟页的常量，没注明来源
- rule-150db57dc0bb｜源码按折叠态切换工具栏图标着色时，目标移植状态判定和两态颜色，不写死一色｜读到：源码在 AppBarLayout 的 OnOffsetChangedListener 里按折叠进度切换工具栏图标着色（展开态白、折叠态主题色）；写错：目标工具栏图标颜色写死一个次要色（如固定的 fillColor），不随滚动折叠态变化
- rule-40af1107f177｜规格锚点列了工具栏着色的实现类时，写前读它取阈值和颜色，不以近似占位推迟｜读到：CollapsingToolbarLayout 折叠头部，规格的源码锚点列了负责工具栏图标着色和折叠切换的实现类；写错：目标用固定的次要文字色图标和 opacity = 折叠比例的实底近似工具栏变色，并登记 UNC 占位推迟
- rule-37b4a36e0639｜复用同族页先例时当草稿逐项核对，标 UNC 的近似不当已验证手法照抄｜读到：规格要求复用另一页已写好的同款实现（「同 page_… 方案」），先例代码或登记里带 forward-ref-uncertain / `UNC` 编号的近似；写错：新页照抄先例的近似（如背景 .height('100%')、无 blur、图标固定次要色、.align 定位），注释称「沿先例已验证手法」，自检没跑已加载 pitfall 条目的 grep

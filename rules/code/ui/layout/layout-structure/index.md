# 源布局里的图文结构

agent 会看到什么：读到源布局 XML 由 ImageView 加 TextView 的菜单行、带标题条背景和插图的卡片、固定高度标题栏、TabLayout 等组件组成；产物里只剩 Text、缺 Image、卡片数少，或保留了源布局里没有的区块只调尺寸

## 规矩

- rule-d5f52e7b68bc｜源端菜单行、按钮由 ImageView 加 TextView 或 drawableLeft 组成时，目标写图标加文字｜读到：弹出菜单行、操作按钮由 <ImageView android:src="@drawable/..."> 加 <TextView> 组成，或标题 TextView 带 android:drawableLeft / android:drawableStart 图标和专用 @color 颜色资源；写错：目标的菜单行、操作栏按钮或分组标题只有 Text(...)，没有 Image($r('app.media....'))，文字颜色和字号也不是源端的颜色资源和尺寸
- rule-6240ea8e2dc1｜源布局是带标题条背景和插图的图文卡时，目标页逐卡迁入标题条和插图、卡数一致｜读到：静态说明页的布局 XML 由多张圆角卡组成：标题 TextView 带 android:background="@drawable/…" 的标题条，卡内或页首尾有 ImageView 的 android:src="@drawable/…" 插图；写错：目标页只用 Text 拼成纯文字卡：没有 Image($r('app.media.…'))，标题只是普通粗体 Text、没有标题条背景，或者卡片数比源布局少
- rule-f35da8555d77｜对齐已有页面时按源布局 XML 列组件清单逐项比对，源端没有的区块替换掉而不是只调尺寸｜读到：源布局 XML 有背景 ImageView、固定高度的标题栏、统计卡片的各个子 TextView、主按钮文案、TabLayout / ViewPager、空态；写错：已有 ArkTS 页面保留了 XML 里没有的区块（linearGradient 渐变头、多出的统计项、列表区和按钮），改动只落在 .height(...)、.margin(...)、按钮宽度上
- rule-5db482f55571｜列表控件带 tools:listitem 时打开那个 item 布局，按它写列表行结构｜读到：源布局里列表控件写 tools:listitem="@layout/…"，行结构在被引用的 item 布局 XML 里；写错：鸿蒙端 ListItem 里只写了几行文字，缺 item 布局里的图标、文字层级和右侧列
- rule-c6825d66b89b｜照源布局逐控件核类型和文案：tv_ 开头的 ImageView 照写关闭图标，hint 取 android:hint｜读到：源布局里 id 像文本控件（如 tv_ 前缀）的其实是 <ImageView>（右上关闭图标）；<EditText> 写了 android:hint；写错：目标把它写成「取消」文字 Button 并和「确定」组成双按钮；TextInput 的 placeholder 用了 toast 文案而不是 android:hint
- rule-74fd808d66f6｜布局 XML 的标题栏、底部按钮和列表项内容，在 ArkUI 页面里逐项写出对应节点｜读到：布局 XML 标题栏容器里有返回图标、居中的标题 TextView、右侧编辑/取消色块，底部有固定高度和边距的按钮；列表项数据是实体加异步加载的摘要（Pair<实体, 摘要?>）；写错：ArkUI 标题用 layoutWeight 左对齐、没有返回图标、编辑写成纯文字；底部按钮高度、边距与源不同；列表项只显示名称和编码，没有摘要
- rule-f38664d0fff9｜按 spec 重写页面时先读 spec 的页面结构或源布局 XML，不保留安卓没有的自创头部｜读到：spec 的页面结构 / Android 可观察事实段或源布局 XML（根 android:background、标题和内容区的 layout_marginTop）写明了顶部结构；写错：重写后保留了基线页面里安卓没有的自创头部（渐变头卡、大号白字加简介），根 .backgroundColor、标题区和内容起点与 spec 不符，报告仍称已对齐源页面
- rule-dc03e6ee68f3｜按钮层的渲染分支对照源布局控件清单，数据缺省时的默认入口也要渲染｜读到：源布局 XML 里按钮层的全部控件（各自的 android:id）；目标布局状态的摆位表；写错：按钮层少了摆位表里某些键的渲染分支，或入口只在缩略图 PixelMap 存在时才渲染，没有数据时不显示

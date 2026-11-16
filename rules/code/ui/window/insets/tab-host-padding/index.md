# 包住 Tabs 的宿主容器上的内边距

agent 会看到什么：读到单 Activity 宿主承载各 Tab Fragment（ViewPager2、TabLayout），源端用 ImmersionBar 沉浸、titleBarMarginTop、transparentStatusBar、windowTranslucentStatus，或 paddingStart / paddingEnd 只写在底栏上；产物里包住整个 Tabs 的容器加了顶部状态栏 padding 或左右 padding

## 规矩

- rule-86c2ae907301｜Tab 宿主按各 Fragment 的状态栏处理逐 Tab 定穿透或避让，不给整列内容加顶部 padding｜读到：源主题 `android:windowTranslucentStatus` 为 true 或用 `ImmersionBar` 沉浸；有的 Fragment 设 `statusBarView(...)` 或放占位 View，有的只调 `statusBarDarkFont`、头图铺到状态栏下；写错：宿主给承载所有 Tab 的整列容器写 `.padding({ top: <状态栏高度> })`，回执记成「前景 inset」
- rule-af547727d6f9｜Tab 子页自带延伸到顶的背景时，宿主内容容器不再统一加顶部 padding｜读到：源端 Tab 子页（Fragment）的头图背景顶对父容器、用状态栏占位只下推前景；写错：宿主承载各 Tab 和底栏的内容 Column 上有 .padding({ top: <顶部避让值> })，把子页背景和前景一起下移
- rule-b81400ed72c2｜源端 Tab 用 titleBarMarginTop 让头图延伸到状态栏下时，宿主去掉顶部避让，标题加避让高度｜读到：宿主 Fragment 里 `ImmersionBar.with(this).titleBarMarginTop(view)`，头图从屏幕顶部画起，顶部栏下移状态栏高度；写错：标题写成固定的 margin({ top: … })，不含状态栏偏移；宿主仍对该 Tab 加顶部避让 padding；报告写 `immersive_safearea_skipped`
- rule-b25f396648fb｜sub_component 只跳过窗口级沉浸设置，页内状态栏占位改成前景容器消费宿主避让值｜读到：源嵌入页用 ImmersionBar.statusBarView(占位) 撑出状态栏高度，内容约束在占位之下；页面元数据 page_type=sub_component、needs_immersive_safearea=false；写错：目标 Stack 里头图背景和前景 Column 都没有状态栏偏移，前景只有源端的 margin；或者给背景和前景一起加了 .padding({ top: … })
- rule-7d395afa124d｜Tab 宿主的内边距放回源端原节点，不加在包住整个 Tabs 的容器上｜读到：宿主布局里 ViewPager2 宽高 match_parent、只设 layout_marginBottom，android:paddingStart / paddingEnd 只写在底部 Tab 栏容器上；写错：目标把 .padding({ top: 状态栏高度, bottom, left, right }) 加在包住整个 Tabs 的 Column 上，所有 TabContent 左右内缩、顶部让出一条状态栏
- rule-6a0e2d199cfd｜补状态栏实色带时宿主是 Tabs，把 Tabs 包进带避让 padding 和底色的 Column，不挂在 Tabs 上｜读到：源 Activity 或它的基类在 onCreate 里把状态栏设成实色；写错：全屏布局的页面把顶部避让 .padding({ top: … }) 和 .backgroundColor(…) 直接挂在 Tabs（或 Swiper 这类由子页面铺满的容器）上，指望 padding 区透出色带

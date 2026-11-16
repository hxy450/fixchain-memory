# Tab 宿主的内边距放回源端原节点，不加在包住整个 Tabs 的容器上

审的是：代码
触发（任一种）：
- 读到：宿主布局里 ViewPager2 宽高 match_parent、只设 layout_marginBottom，android:paddingStart / paddingEnd 只写在底部 Tab 栏容器上；写错的样子：目标把 .padding({ top: 状态栏高度, bottom, left, right }) 加在包住整个 Tabs 的 Column 上，所有 TabContent 左右内缩、顶部让出一条状态栏
适用范围：把 ViewPager2 / ViewPager 加底部 Tab 栏的宿主 Activity 迁成 ArkUI Tabs 宿主页时
做法：
- 左右内边距只加在对应源端底部 Tab 栏的那个节点上（自定义 Tab 栏的容器或 tabBar 的构建内容），Tabs 和 TabContent 横向铺满
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- padding(value: Padding | Length | LocalizedPadding): T：内边距加在哪个节点上，就只内缩那个节点的内容（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.padding）
未核实：卡里最终修复（取消该 Tab 的顶部和左右内边距）注明未上机验证
来源：1 张卡，1 个应用
- case-06c7df8f8d85e13580ac（app_hnaccurateweather_live_android）：做法第 1 步 ← 建议 3、诊断

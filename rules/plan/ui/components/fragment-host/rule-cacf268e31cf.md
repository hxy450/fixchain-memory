# 把 fragment 内容交给共享组件时，移交项写明 fragment 根的 padding 和背景由谁实现

审的是：计划与派工
触发（任一种）：
- 读到：fragment 布局的根 LinearLayout 写了 android:padding*（或背景），承载它的 ViewPager 没有 padding；页面转换把 fragment 内容交给共享组件承载；写错的样子：移交项只写了共享组件名和槽位，没写 fragment 根布局的 padding、背景由宿主容器还是共享组件实现
适用范围：页面转换把 fragment 拆成宿主页容器和共享组件、通过移交项交给别的切片实现时
做法：
- 移交项里写一句：fragment 根布局的 padding（四边各取哪个尺寸资源）和背景由「宿主容器」或「共享组件」其中一方实现，另一方不写
来源：1 张卡，1 个应用
- case-4e7e0e12d7b6b08c08b0（Privacy Friendly 2048）：做法第 1 步 ← 建议 3

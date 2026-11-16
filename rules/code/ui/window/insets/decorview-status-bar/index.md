# DecorView 上的状态栏底色和顶部避让

agent 会看到什么：读到源端在 DecorView 上 setBackgroundColor 画状态栏底色、setPadding(0, statusBarInsets.top, 0, 0) 避让状态栏，产物里是 setWindowSystemBarProperties 的 statusBarColor、页面容器的顶部 padding 或布局输出上的 Y 平移

## 规矩

- rule-6a32b9ec57d3｜源端根视图 padding 避让状态栏时，代码给画布容器加顶部 padding，不在布局输出上做 Y 平移｜读到：源端 DecorView.setPadding(0, statusBarInsets.top, 0, 0)，内容 View 的 onSizeChanged(width, height) 直接调布局方程；skill 映射写 view.setPadding → padding({ top: … })；写错：Canvas 铺满整页、容器没有顶部 padding，布局用全画布高算，再给各 Y 字段加 topShift（如 vp2px(顶部避让)）；onSizeChanged 多了 topShift 参数，注释写「含安全区 topShift」
- rule-5ba6271e2776｜页面自绘状态栏底色时，系统栏 statusBarColor 设透明，不给系统栏着色｜读到：源端状态栏区域底色由 DecorView.setBackgroundColor 绘制；规格或派工要求「核验系统栏配色是否含 #…，缺则补」；写错：EntryAbility 里 setWindowSystemBarProperties({ statusBarColor: '#ff…' }) 把底色交给系统栏，页面容器却没有底色和顶部 padding

# 全屏页贴底元素的导航条避让

agent 会看到什么：读到贴底按钮行、底部弹层的根布局只有固定的 android:paddingBottom / layout_marginBottom；产物里全屏页贴底元素的 .padding({ bottom: … }) 没加导航条避让值

## 规矩

- rule-71a70d8b43b4｜全屏布局页的贴底按钮行，不因安卓 XML 没有底部间距就省掉 bottomPadding｜读到：安卓布局 XML 里贴底的按钮行和标题只有固定的 android:padding / layout_marginBottom，没有导航栏间距；写错：目标页在 setWindowLayoutFullScreen(true) 下，贴底按钮行的 .padding({ bottom: N }) 和贴底元素的底距没加底部避让值，或者声明了底部避让变量却没在任何地方用
- rule-333f08a143df｜全屏沉浸页里贴屏底的 bindSheet 内容，由宿主经 @Param 注入导航条避让值加到底部 padding｜读到：源端 BottomSheetDialogFragment 的布局根只写 android:paddingBottom；写错：目标 sheet 组件根容器只写 .padding({ bottom: 源值 })，没有避让参数；页面测得的底部安全区只用在页面自己的控件上

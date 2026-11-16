# 根视图按状态栏 insets 设顶部 padding

agent 会看到什么：源 Activity 在 DecorView（根视图）上按 statusBarInsets.top 调 setPadding、有的还 setBackgroundColor 自绘状态栏底色，规格里写的是状态栏沉浸、安全区避让或系统栏底色

## 规矩

- rule-ba516257f960｜根视图按状态栏 insets 设顶部 padding 时，规格写内容区从状态栏下沿开始、布局高度扣除状态栏｜读到：源 Activity 给 DecorView（根视图）setPadding(0, statusBarInsets.top, 0, 0)，内容 View 在 onSizeChanged(width, height) 里按自身尺寸调 getLayout 之类的布局方程；写错：规格写「状态栏沉浸 + 顶部安全区避让，布局方程沿用全屏尺寸」，或要求在布局输出上整体做 Y 平移
- rule-0b09f425734d｜DecorView 自绘状态栏底色且页面有遮罩弹窗时，规格映射为页面容器背景加顶部 padding、系统栏透明｜读到：源端（如 Android 15+ 分支）在 DecorView 上 setBackgroundColor(color) 并 setPadding(top=statusBarInsets.top)，状态栏区域的底色由应用根视图绘制；页面里有带遮罩的弹窗；写错：规格、验收条目或台账把这处底色映射为 window.setWindowSystemBarProperties({ statusBarColor })，写「系统栏底色 #…」

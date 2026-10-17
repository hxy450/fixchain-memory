# ui/state/binding

状态到控件的绑定与刷新：随状态变的参数不作 @Builder 值参、事件给出的目标值直写、按状态显隐、乐观更新。

[上一级](../index.md)

## 本级经验

- [Tab 默认选中只初始化一次，items 更新仅同步高亮](lesson-b6abeeb9b9476b1f1f4d.lesson.md) · 阶段：execute · 信号：@Param, @Event, @Monitor, selectedIndex
- [setVisibility 分支随状态迁移，GONE 不渲染](lesson-43a9050245b1afa165bf.lesson.md) · 阶段：execute/repair · 信号：setVisibility, Visibility.Hidden, GONE, setText
- [上抛自身可见性的组件常建，不包 if/None](lesson-3a00fd66c5188f5cfdf4.lesson.md) · 阶段：execute · 信号：Visibility.None, visibility="gone", aboutToAppear, Fragment
- [乐观更新先翻转本地状态再发请求，回调只回填真值](lesson-18c8e7630a96d66540bc.lesson.md) · 阶段：execute · 信号：isFavorite, isLiked, onSuccess, @Local
- [回调中置位的状态按回调门控并补控件过滤](lesson-af89611fa71ea0eb6f45.lesson.md) · 阶段：execute · 信号：onQueryTextSubmit, SearchView, onSubmit, isLoading
- [宿主标题栏与 H5 导航栏按页面状态双向决定显隐](lesson-1a5fbc237ad071a62aaa.lesson.md) · 阶段：execute/repair · 信号：runJavaScript, onOverrideUrlLoading, onTitleReceive, onPageEnd
- [开关事件目标值直传 setter，不用 toggle 取反](lesson-40fc63b124b4a44e7a9f.lesson.md) · 阶段：execute · 信号：onToggleChange, isOn, @Event, @Param
- [状态派生值不传 @Builder，改 @Param 子组件](lesson-8d2979542fa2cd65150c.lesson.md) · 阶段：execute/repair · 信号：@Builder, @Param, @ComponentV2, Repeat

# process/inferred-not-traced

凭名字、所在模块、import 或调用点推断语义，没有追到定义、委托终点与实际绑定

[上一级](../index.md)

## 本级经验

- [推断默认选中前读默认值回调、过滤函数与回退条件](lesson-e7a9842a56aa53621d27.lesson.md) · 阶段：execute · 信号：BasePage, override fun, defaultSelection
- [源端层层委托时追到最终实现再写规格与代码](lesson-4606ccc434e247d4a240.lesson.md) · 阶段：spec/execute · 信号：DialogHelper, DAO, Repository, LazyColumn
- [辅助谓词与 getter 读到定义再翻译，不按名字推断](lesson-b3f534eb740a768d95a6.lesson.md) · 阶段：spec/execute · 信号：isPlayingState, playPause, LiveData&lt;String&gt;, PAUSED
- [页面入口只按布局与页面类实际绑定推导，不补源端没有的控件](lesson-76aa7901a0ae1af9d544.lesson.md) · 阶段：spec/verify/repair · 信号：initView, setOnClickListener, ViewModel, onClick
- [页面归属按实际 Service 调用判定，不按模块默认](lesson-ad7d770bd5b826e58516.lesson.md) · 阶段：spec/plan · 信号：resolve_by, Retrofit, Service, page_id

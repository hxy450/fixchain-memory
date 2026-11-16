# 页面读 @ObservedV2 模型的 @Trace 状态

agent 会看到什么：读到 @ObservedV2 / @Trace 的模型或 store；产物里页面把它的字段拷进 @Local、靠 onPageShow 或手动 refresh 同步，或 VM 异步写 @Trace 列表

## 规矩

- rule-28e57810f13d｜页面显示的业务状态直接读 @ObservedV2 模型的 @Trace 字段，不复制成 @Local 副本｜读到：决策台账或规格写某个模型统一管理状态、并向其他功能提供数据；状态管理约定是 @ObservedV2 类的 @Trace 属性变化触发刷新；写错：页面把模型的多个字段复制进 @Local，在每个处理函数调用模型后用一个同步方法手动拷贝一遍，build 读的是这些副本
- rule-90c10f213373｜@ComponentV2 子组件不用 onPageShow，也不退回手动 Refresh 按钮，改用响应式绑定｜读到：页面组件是 @ComponentV2 子组件（不是 @Entry），数据来自会被异步加载或回调更新的 store；写错：写了 onPageShow() 刷新（子组件里不触发），或删掉 onPageShow 后只留 aboutToAppear 和 Refresh 按钮上的手动 refresh() 拷贝
- rule-9c5103eb2c73｜加请求代次时，VM 内部异步写 @Trace 列表也要校验代次、日期和筛选值｜读到：VM 的异步加载方法在 await 查询返回后直接给 @Trace 列表赋值；写错：只在页面提交结果前比对请求代次，VM 内部写 @Trace 列表时没有校验代次、请求的日期和筛选值，旧请求的结果可能覆盖新数据
- rule-b4ca8c9f52b7｜给按值渲染的 @Builder 行写异步数据时，原位更新 @Trace 字段，不整体替换也不自赋值｜读到：已有 @Builder 行按值取一个 @ObservedV2 实例渲染，数据在定位、加载等异步回调里才到；写错：回调里 this.item = new …(…) 整体替换实例，或写 this.item = this.item 自赋值想触发刷新
- rule-91e20c64ec34｜源端每次变更都生成新列表时，ArkTS 入队出队都整体重新赋值数组，不用 push｜读到：Kotlin 的 MutableStateFlow<List<…>> 用 update { it + item } 入队、filterNot 出队，每次生成新列表；写错：ArkTS 生产方入队用 .push(...) 原位修改 @Trace 数组，出队却重新赋值，两种变更信号不一致
- rule-c9e56287fb20｜上游已有 @Trace 全局存储时，页面同步读它，不用 @Local 快照加 aboutToAppear 异步赋值｜读到：派工写明某个全局存储已就绪，或读到的目标存储里有 @Trace 当前值字段；源页面在提交前用 observeAsState 读到的当前值做守卫判断；写错：页面写 @Local 布尔或对象快照（初值 false 或兜底哨兵），在 aboutToAppear 里异步查库 .then 赋值，再用快照做守卫；照抄兄弟页的旧写法
- rule-d313f606035b｜源端用 observeAsState / LiveData 读守卫依赖的状态时，目标出口给同步可读的 @Trace 存储｜读到：源端公共读取函数是 observeAsState() + derivedStateOf { current ?: 兜底哨兵 } 这类响应式读取（或 LiveData / StateFlow），写操作前的守卫依赖它；写错：目标公共函数写成 async 一次性查库，注释要求调用方在 aboutToAppear 里拉取后持本地副本

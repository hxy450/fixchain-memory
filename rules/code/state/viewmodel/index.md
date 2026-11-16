# ViewModel 与数据层

源端 ViewModel 用 LiveData / Flow 发布页面数据，数据来自 Repository、Room Dao、assets 文本、引擎或回调实现类，目标端有 VM、store、gateway 的字段从哪赋值、何时赋值、状态初值、addListener 订阅、写后刷新和给 UI 的门面接口时

## 触发族

- [ViewModel 发布的数据在目标端的来源和赋值时机](viewmodel-state-source/index.md)（9 条）：读到源 ViewModel 用 LiveData / MutableLiveData 发布页面数据（选中项变化时的附带查询、单独持久化的一项、text 前缀的格式化字段、WorkInfo 聚合、初始化时同步写入、只在 success 里写值），Fragment observe 后绑定控件；产物里目标 VM / gateway 的字段从哪赋值、什么时候赋值（await 之前或之后、catch 里置 0、map.delete）
- [列表、选项和页面模型数据的来源](list-data-source/index.md)（5 条）：读到源 ViewModel / Repository 从 assets 文本解析层级数据、按 <Bean, ViewModel> 数据源给 RecyclerView 发布选项列表、几个 RecyclerView 各绑一份列表、公开多个取数方法，UI 模型里有多组列表字段；产物里写死的数组字面量、几个分组的 ForEach 渲染同一个数组、网关只给部分字段赋值、只接了主接口
- [单例数据层的 addListener 订阅](repository-listener/index.md)（2 条）：读到源端用 LiveData / Flow 的 observeAsState、collectAsState 观察数据（随生命周期自动结束），交回的代码在应用级单例的数据层上写 addListener / removeListener
- [只在事件分支里写的状态字段初值](event-only-initial-value/index.md)（1 条）：读到源端只在某个事件分支（如 BluetoothGatt 断连回调）里写入的占位串，其余时候写读数；产物里状态类 @Trace 字段的初值直接用了这个占位常量
- [VM 到 UI 的门面接口](vm-ui-facade/index.md)（1 条）：读到源端回调实现类的 @Override 回调里直接调 UI 类的方法（显示控件、刷新屏上图标）；产物里 VM 定义的 UI 门面 interface 和 sink 缺了这些方法，下游只能按缺项的接口接线
- [引擎持有的模式在界面上的镜像状态](engine-mirror-state/index.md)（1 条）：读到源端某个模式（如是否录像）只存在引擎里，冷启动时引擎按偏好恢复、Intent 入口也能设；产物里 VM 另设的 @State / @Trace 镜像状态的默认值，以及就绪回调里有没有从引擎回读
- [Room LiveData 观察的表在目标存储里的刷新](room-livedata-refresh/index.md)（1 条）：读到源端当前数据来自 Room @Dao 返回的 LiveData，ViewModel 的写方法只写库、靠 LiveData 重新发射；产物里目标存储的每个写方法有没有刷新内存里的 @Trace 当前值并广播

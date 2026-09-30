# 源页面从 arguments、Intent extras 或缓存接收的实体键与数据，在目标以显式入参承接并由宿主真实传入

ID：`lesson-289cab2abd4268b26ce0` · 版本：3

[本主题](index.md)

## 何时使用

界面转换与接线阶段，为 Tab 子组件、多实例子页或详情页定义入参，并在宿主或调用方挂载、跳转时；撤回或调整宿主传给子页面的参数时

## 适用情境

源 Fragment 经 newInstance/arguments 或宿主 setCurrentCity 获得城市、ID 等实体键，详情 Activity 经 Intent Serializable 或首页缓存拿到首页数据；目标子组件以 @Param 或路由参数接收，宿主可能新增无参 Builder 挂载，或子组件改读全局选中状态。也包括子页面声明带默认值的状态参数（如当前分组类型），源端据此切换新增按钮与条目元信息，宿主在接线中写了该参数又删掉。

## 原因

入参没有真实来源时，子组件只能用默认值：城市为空就在请求前进入错误态，多实例子页读全局选中城市导致串城，详情页的列表只剩静态占位。来源为同一应用三处：宿主新增吞掉参数的无参 Builder 挂载 15 日 Tab；天气页组件不声明城市入参、多实例容器丢弃插槽参数；空气质量与天气趋势详情页的入参只有城市与坐标，首页 15 日数据没有任何交接来源。另一应用的宿主接线删掉了当前空间类型的传参，子页面永远取默认值 0：新增按钮被隐藏或拦截，具体空间下仍显示条目空间信息；删除后既没有改用其他派生，也没有在回执中列为未决。

## 做法

1. 列出源页面全部入参来源（arguments、Intent extras、宿主注入、读取的缓存），目标以 @Param 或路由参数一一承接；列表类状态要有等价数据来源，不只留静态占位。
2. 宿主接线时逐项对照子组件的 @Param/@Event 声明，默认值为空或 0 且组件会据此报错的参数，在宿主找到真实来源再传入；不新增吞参数的无参 Builder，也不让子组件改读全局选中状态。
3. 撤回某个传参时同时给出替代派生（如按当前选中项是否为空判断）或在交接中列为未决，不让子页面静默落回默认值。

## 可选检查

- 从宿主进入该页时，组件收到的实体键有效（如 cityCode > 0），事件回调已绑定到导航。

## 来源（按需复核）

- [case-1cfad6c2eaf32070939a](../../../../store/cases/case-1cfad6c2eaf32070939a/22c647b810d09efec62c8bd0f841bcc9e4f190e1a6f8e9f9a5ac20ff7e81d33d.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`22c647b810d09efec62c8bd0f841bcc9e4f190e1a6f8e9f9a5ac20ff7e81d33d`
- [case-35171ce59437beebb0ea](../../../../store/cases/case-35171ce59437beebb0ea/e1713f686b8590a165e453057fb4f6b19ec40d66876b9ae7c88631b33bc7ced5.json) · 结论：diagnosis, recommendation:2, recommendation:3
  卡片版本：`e1713f686b8590a165e453057fb4f6b19ec40d66876b9ae7c88631b33bc7ced5`
- [case-5d12548f9d559985c27d](../../../../store/cases/case-5d12548f9d559985c27d/608dbd2b1d6e008fc1af336ba33a164d3fc8a14bc9efa8aaf99219ea3d4be3a0.json) · 结论：diagnosis
  卡片版本：`608dbd2b1d6e008fc1af336ba33a164d3fc8a14bc9efa8aaf99219ea3d4be3a0`
- [case-e7af91622703010ed47f](../../../../store/cases/case-e7af91622703010ed47f/ca3bef0c958a548e08983f174d26cced13cdd7ea2a57be3536b0c7ea8d2a7c32.json) · 结论：recommendation:3
  卡片版本：`ca3bef0c958a548e08983f174d26cced13cdd7ea2a57be3536b0c7ea8d2a7c32`

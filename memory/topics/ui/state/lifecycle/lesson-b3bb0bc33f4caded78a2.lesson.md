# 源页面由事件订阅或结果回调触发的重新加载要迁成订阅；Navigation 根页、Tab 内容或经 router 返回的 @Entry 页在子页返回时不会再走 aboutToAppear

ID：`lesson-b3bb0bc33f4caded78a2` · 版本：6 · 阶段：execute/converge · 主题：[ui/state/lifecycle](index.md)

概要：重载入口改订阅，子页返回不触发 aboutToAppear

信号：`aboutToAppear`, `onShown`, `onPageShow`, `pushPathByName`, `router.back`, `EventBus`, `@Subscribe`, `ActivityResult`

## 何时使用

ViewModel 与页面接线阶段，决定目标页由哪些入口触发数据重新加载时；流程闭环阶段从该页新增 push 子流程时

## 适用情境

源 Fragment 用 EventBus @Subscribe（登录成功、记录变化等）和 ActivityResult 回调重拉数据；目标页是 Navigation 下常驻的根内容或 Tab 页，登录、详情等子页用 pushPathByName 覆盖后 pop 返回；工程已有会话状态与应用事件总线。 也包括列表页经 router.pushUrl 打开新增/编辑页，对方保存后 router.back 返回，列表数据只在 aboutToAppear 拉取。

## 原因

aboutToAppear 只在组件创建时执行；子页 pop 返回时根页组件没有重建，只在 aboutToAppear 或 activate 里拉数据，等于只加载一次。来源中验收条目写明“源：登录/记录事件 → 标：刷新函数”，实现者却只把它落实成丢弃迟到响应的 token；后续扩展入口的实现者又假设“返回首页会重新刷新”，保存、删除记录也不发刷新事件。真机登录后记录页已有数据，首页统计仍为 0。另一应用中，个人中心是常驻 Tab，接线者没打开源 Fragment、只在 aboutToAppear 加载，规格“登录成功后重载任务数据”的条款没有落实；工程里登录成功事件已有发布方，却没有任何消费者，登录后返回仍显示未登录。 另一应用的地址列表沿用占位版只在 aboutToAppear 加载的写法，新增地址保存返回后列表不变，补 onPageShow 重载后才显示。

## 做法

1. 把源页面所有重新加载的入口列成清单（生命周期回调、事件订阅、结果回调），在目标 ViewModel 为每项写对应订阅（如会话状态订阅、应用事件总线订阅），并确认发布方存在：保存、删除等成功处发布刷新事件。
2. 需要“返回后刷新”时用订阅或 NavDestination 的 onShown 等可见性回调，不依赖 aboutToAppear；订阅在销毁时注销，不因页面暂时不可见的标志而丢弃事件；经 router 返回的 @Entry 页用 onPageShow 重载，并区分首次加载与返回刷新的 loading 状态。重写占位页时不沿用占位版的生命周期写法。

## 可选检查

- 登录后返回该页、保存或删除记录后返回该页，数据无需重进即更新。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [PowerShell 读文件带 UTF8 编码，乱码视为未读](../../../process/unloaded-input/lesson-6a3a7f46c8fec282affa.lesson.md)（共享 1 张卡）
- [功能对齐以代码落点为准，空回调不算实现](../../../process/claimed-without-receipt/lesson-9147be4d87153de9c5b6.lesson.md)（共享 1 张卡）
- [选择器回填的省市区多级值实现选择流程一次写回](../../interaction/selectors/lesson-b845647090bfeac053ed.lesson.md)（共享 1 张卡）

来源支持：3 张卡 · 3 次迁移 · 3 个应用

## 来源（按需复核）

- [case-03947f1730e7f74c490f](../../../../../store/cases/case-03947f1730e7f74c490f/275699fba1617e98eab38ad764c023e51e92270e7462d59018314a432e6d3fa7.json) · 结论：diagnosis, rec-4088100666, rec-e393ead8b9
  卡片版本：`275699fba1617e98eab38ad764c023e51e92270e7462d59018314a432e6d3fa7`
- [case-46ac36102451125de693](../../../../../store/cases/case-46ac36102451125de693/86c57b38cd3897abac8b2c1d68ca50b219ea6c13be75dcd1fd0045e39be6fba6.json) · 结论：diagnosis, rec-1cf72bd244
  卡片版本：`86c57b38cd3897abac8b2c1d68ca50b219ea6c13be75dcd1fd0045e39be6fba6`
- [case-6077d9f3d384e0cb140f](../../../../../store/cases/case-6077d9f3d384e0cb140f/d4db908aa23c5fb9494c808b0986c8d73a46e81f50b35e70e79146b6235a6d02.json) · 结论：diagnosis, rec-25c811c903, rec-507f9eff68, rec-2d228a68a9
  卡片版本：`d4db908aa23c5fb9494c808b0986c8d73a46e81f50b35e70e79146b6235a6d02`

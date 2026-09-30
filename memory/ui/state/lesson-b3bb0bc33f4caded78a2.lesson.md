# 源页面由事件订阅或结果回调触发的重新加载要迁成订阅；Navigation 根页或 Tab 内容在子页返回时不会再走 aboutToAppear

ID：`lesson-b3bb0bc33f4caded78a2` · 版本：2

[本主题](index.md)

## 何时使用

ViewModel 与页面接线阶段，决定目标页由哪些入口触发数据重新加载时；流程闭环阶段从该页新增 push 子流程时

## 适用情境

源 Fragment 用 EventBus @Subscribe（登录成功、记录变化等）和 ActivityResult 回调重拉数据；目标页是 Navigation 下常驻的根内容或 Tab 页，登录、详情等子页用 pushPathByName 覆盖后 pop 返回；工程已有会话状态与应用事件总线。

## 原因

aboutToAppear 只在组件创建时执行；子页 pop 返回时根页组件没有重建，只在 aboutToAppear 或 activate 里拉数据，等于只加载一次。来源中验收条目写明“源：登录/记录事件 → 标：刷新函数”，实现者却只把它落实成丢弃迟到响应的 token；后续扩展入口的实现者又假设“返回首页会重新刷新”，保存、删除记录也不发刷新事件。真机登录后记录页已有数据，首页统计仍为 0。另一应用中，个人中心是常驻 Tab，接线者没打开源 Fragment、只在 aboutToAppear 加载，规格“登录成功后重载任务数据”的条款没有落实；工程里登录成功事件已有发布方，却没有任何消费者，登录后返回仍显示未登录。

## 做法

1. 把源页面所有重新加载的入口列成清单（生命周期回调、事件订阅、结果回调），在目标 ViewModel 为每项写对应订阅（如会话状态订阅、应用事件总线订阅），并确认发布方存在：保存、删除等成功处发布刷新事件。
2. 需要“返回后刷新”时用订阅或 NavDestination 的 onShown 等可见性回调，不依赖 aboutToAppear；订阅在销毁时注销，不因页面暂时不可见的标志而丢弃事件。

## 可选检查

- 登录后返回该页、保存或删除记录后返回该页，数据无需重进即更新。

## 来源（按需复核）

- [case-46ac36102451125de693](../../../store/cases/case-46ac36102451125de693/86c57b38cd3897abac8b2c1d68ca50b219ea6c13be75dcd1fd0045e39be6fba6.json) · 结论：diagnosis, recommendation:2
  卡片版本：`86c57b38cd3897abac8b2c1d68ca50b219ea6c13be75dcd1fd0045e39be6fba6`
- [case-6077d9f3d384e0cb140f](../../../store/cases/case-6077d9f3d384e0cb140f/d4db908aa23c5fb9494c808b0986c8d73a46e81f50b35e70e79146b6235a6d02.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`d4db908aa23c5fb9494c808b0986c8d73a46e81f50b35e70e79146b6235a6d02`

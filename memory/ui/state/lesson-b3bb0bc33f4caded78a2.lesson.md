# 源页面在 onResume、事件订阅或结果回调里重新加载数据时，按目标挂载类型接可见性回调或订阅，不只在 aboutToAppear 加载

ID：`lesson-b3bb0bc33f4caded78a2` · 版本：6

[本主题](index.md)

## 何时使用

ViewModel 与页面接线阶段，决定目标页由哪些入口触发数据重新加载时；从常驻页新增 push 子流程时；把 Activity 的 onStart/onResume 初始化映射到目标页面回调时

## 适用情境

源 Fragment/Activity 用 EventBus @Subscribe（登录成功、记录变化等）、ActivityResult 回调或 onStart/onResume 重拉数据、重读 Intent、重建列表；目标页是 Navigation 下常驻的根内容、Tab 页、NavDestination，或经 router.pushUrl 打开新增/编辑页后 router.back 返回的 @Entry 页，数据只在 aboutToAppear 或一次性的 onReady 拉取；工程可能已有会话状态与应用事件总线。

## 例外与边界

- 源端只在 onCreate 加载一次，没有可见性、事件或结果回调触发的重载：保持一次性加载
- 只在页面可见期才应接收的监听（硬件、标签）属于注册与注销的作用域决策，按可见期在 onShown/onHidden 成对处理，不在本条的重载清单里展开

## 原因

aboutToAppear 只在组件创建时执行；子页 pop 返回或 router.back 时，被覆盖的页面组件没有重建，只在 aboutToAppear 或一次性回调里拉数据，等于只加载一次。源端的重载常分散在事件订阅与结果回调里，只迁生命周期回调会漏掉它们；保存、删除成功处不发布事件时，订阅方也收不到。

## 做法

1. 把源页面所有重新加载的入口列成清单（生命周期回调、事件订阅、结果回调），在目标 ViewModel 为每项写对应订阅（如会话状态订阅、应用事件总线订阅），并确认发布方存在：保存、删除等成功处发布刷新事件。
2. 按目标挂载类型选返回刷新入口：NavDestination 用自身的 onWillShow/onShown；经 router 返回的 @Entry 页用 onPageShow；Navigation 根内容与 Tab 子组件没有自己的页面显隐回调，由宿主把可见变化下发或订阅源端等价事件触发刷新：Tab 内容可用 TabContent.onWillShow（含页面切换与前后台切换，tab_content.d.ts，API 12）；Navigation 根内容可接 Navigation.onNavBarStateChange（导航栏可见性变化），子页覆盖与返回时是否触发先在设备上核对。区分首次加载与返回刷新的 loading 状态。
3. 订阅在组件销毁时注销，不因页面暂时不可见的标志丢弃事件；重写占位页时不沿用占位版的生命周期写法。
4. onStart/onResume 中每次可见都执行的初始化（重读 Intent、重建列表、校验目录）映射到 onWillShow/onShown，从后台回前台由 onShown 的 VisibilityChangeReason.APP_STATE 区分；用“进入子页再返回”“切后台再回前台”两条路径自查。

## 可选检查

- 登录后返回该页、保存或删除记录后返回该页，数据无需重进即更新。

来源支持：4 张卡 · 4 次迁移 · 4 个应用

## 来源（按需复核）

- [case-03947f1730e7f74c490f](../../../store/cases/case-03947f1730e7f74c490f/275699fba1617e98eab38ad764c023e51e92270e7462d59018314a432e6d3fa7.json) · 结论：diagnosis, recommendation:3, recommendation:4
  卡片版本：`275699fba1617e98eab38ad764c023e51e92270e7462d59018314a432e6d3fa7`
- [case-46ac36102451125de693](../../../store/cases/case-46ac36102451125de693/86c57b38cd3897abac8b2c1d68ca50b219ea6c13be75dcd1fd0045e39be6fba6.json) · 结论：diagnosis, recommendation:2
  卡片版本：`86c57b38cd3897abac8b2c1d68ca50b219ea6c13be75dcd1fd0045e39be6fba6`
- [case-6077d9f3d384e0cb140f](../../../store/cases/case-6077d9f3d384e0cb140f/d4db908aa23c5fb9494c808b0986c8d73a46e81f50b35e70e79146b6235a6d02.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`d4db908aa23c5fb9494c808b0986c8d73a46e81f50b35e70e79146b6235a6d02`
- [case-7d097177e497ea9e202c](../../../store/cases/case-7d097177e497ea9e202c/4c5e7396ce9a9a0eac126b95b23ab3c18f03dc352495dec2fa11f218b7dfad3a.json) · 结论：diagnosis, recommendation:2
  卡片版本：`4c5e7396ce9a9a0eac126b95b23ab3c18f03dc352495dec2fa11f218b7dfad3a`

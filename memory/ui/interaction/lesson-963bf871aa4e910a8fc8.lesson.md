# 源端在触发瞬间读取锚点窗口位置时，目标在点击回调里即时取坐标，onAreaChange 缓存只作兜底；锚点取源端传入的同一元素

ID：`lesson-963bf871aa4e910a8fc8` · 版本：5

[本主题](index.md)

## 何时使用

界面实现与修复阶段，为从点击处发出的动效或气泡（完成彩纸、锚点提示）确定起点坐标与锚点元素时

## 适用情境

源端在动效或弹窗被调用时用 getLocationInWindow 读取传入锚点 View 的当下窗口中心；目标列表项存在 translate 平移、LazyForEach/Repeat 节点复用或弹层内滚动，写者准备用 onAreaChange 缓存控件位置。

## 原因

onAreaChange 缓存的是布局时的位置，不含之后的平移，也会在节点复用后过期；把整颗按钮或整行当锚点又会偏离源端取的内部图标。手指坐标可落在元素任意位置，与源端取的元素中心不是同一个点。

## 做法

1. 源端取锚点中心（getLocationInWindow 加宽高一半）时，在点击回调里即时取起点：用 getUIContext().getComponentUtils().getRectangleById(锚点 id) 查同一锚点当下的窗口位置、尺寸与平移（ComponentInfo 的 windowOffset、size、translate）求中心，与源端取同一点（d.ts 未写明 windowOffset 是否已含 translate，先用一次已平移的锚点核对）；或取本次手势坐标（如 GestureEvent.fingerList[0].globalX/globalY），它落在点击处而非元素中心。onAreaChange 缓存只在两者都取不到时兜底，并与覆盖层宿主的坐标系统一换算。
2. 核对源端实际传入的锚点是哪个 View（勾选区、按钮内的完成图标），目标取同一元素，而不是整颗按钮或整行。
3. 修锚点回归时以源端调用语义和真机多场景点验（首项与非首项、展开与折叠、弹层内）为准，不以仓内其他页面的写法推翻已验证的坐标修正。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-51d51ad98738e338df19](../../../store/cases/case-51d51ad98738e338df19/4b4648a54d0b19a84c842088554c0b057c5c8941db9a7d98ae885a39678a9db7.json) · 结论：diagnosis, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`4b4648a54d0b19a84c842088554c0b057c5c8941db9a7d98ae885a39678a9db7`

# 源端在触发瞬间读取锚点窗口位置时，目标在点击回调里取本次手势坐标或即时查询，onAreaChange 缓存只作兜底；锚点取源端传入的同一元素

## 何时使用

界面实现与修复阶段，为从点击处发出的动效或气泡（完成彩纸、锚点提示）确定起点坐标与锚点元素时

## 适用情境

源端在动效或弹窗被调用时用 getLocationInWindow 读取传入锚点 View 的当下窗口中心；目标列表项存在 translate 平移、LazyForEach/Repeat 节点复用或弹层内滚动，写者准备用 onAreaChange 缓存控件位置。

## 例外与边界

- 触发写在 onClick 上时，回调参数 ClickEvent 自带本次点击相对应用窗口左上角的 windowX、windowY，取它就是本次手势坐标，不必为了拿 fingerList 改成 TapGesture；代码里已经在点击回调中取事件坐标的写法保留。

## 原因

onAreaChange 缓存的是布局时的位置，不含之后的平移，也会在节点复用后过期；把整颗按钮或整行当锚点又会偏离源端取的内部图标。来源中彩纸起点多次偏离点击处、跑到顶部；修复者一度以“仓内其他页面都用 onAreaChange”为据删掉手势坐标修正，并写入禁止它的静态测试，随后同类问题两次复发。

## 做法

1. 在点击回调中优先取本次手势坐标（如 GestureEvent.fingerList[0].globalX/globalY）或即时查询组件位置；onAreaChange 缓存只在无触点时兜底，并与覆盖层宿主的坐标系统一换算。
2. 核对源端实际传入的锚点是哪个 View（勾选区、按钮内的完成图标），目标取同一元素的中心，而不是整颗按钮或整行。
3. 修锚点回归时以源端调用语义和真机多场景点验（首项与非首项、展开与折叠、弹层内）为准，不以仓内其他页面的写法推翻已验证的坐标修正。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕GestureEvent.fingerList 用于 TapGesture 和 LongPressGesture；触屏手势里包含触发事件的所有触点，鼠标或触摸板发起的手势只有一条记录
- 〔做法第 1 步〕FingerInfo.globalX、globalY 是相对应用窗口左上角的坐标，单位 vp
- 〔原因 / 做法第 1 步〕onAreaChange 只响应布局变化导致的组件大小、位置变化；translate、offset、markAnchor、scale、transform 这类绘制变化不触发回调，回调给出的位置不含之后的平移
- 〔做法第 1、2 步〕Area.globalPosition 是目标元素左上角在当前窗口坐标系中的位置，Area.position 是相对父元素的位置；元素中心要再加上半宽、半高
- 〔适用情境 / 做法第 2 步〕View.getLocationInWindow 在调用当下把这个 View 自身的位置换算到所在窗口的坐标系，不读事先缓存的值
- 〔原因〕用 onAreaChange 缓存的控件位置作动效起点时，列表项发生平移或 LazyForEach 节点复用后，起点偏离点击处、跑到顶部

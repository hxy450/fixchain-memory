# 源页面由点击回调经 ViewModel 副作用导航时，逐个导航出口在目标 onClick 落实际跳转与参数，不留只含注释的回调

## 何时使用

界面实现与返修阶段，为页面中的卡片、列表项、空状态按钮编写点击处理与跨页跳转时

## 适用情境

源 Fragment 的点击回调触发 ViewModel 副作用（如 OpenTripDetail(id)、OpenCreateTrip），再由副作用处理函数调 findNavController().navigate 并带 bundleOf 参数；目标页面自行用 router 或 NavPathStack 跳转。

## 原因

导航写在副作用处理函数里，只对齐可见 UI 元素时容易漏掉“点击→跳转”；回调体只有 // Navigate… 注释时，页面看似接了事件，按 TODO: 检索也发现不了，对齐报告却记成完成。来源中生成期首页卡片与待办都没有 onClick；返修轮读到了源码的两条副作用，仍只写注释占位并报告已对齐。

## 做法

1. 从源端副作用处理函数反查每个 effect 的触发者，列出“可交互元素 → 目标页 + 参数”清单（例如卡片、整项待办 → 详情页(id)，空状态创建按钮 → 编辑页），逐项写成实际跳转调用，并确认目标页已登记或已在导航映射中。
2. 回调体不写只有注释的占位；当前确实无法实现时按工程的移交约定登记，并如实报告未完成。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕RouterOptions.url 是目标页面的路径，取自页面列表（如 pages/detail/detail）；RouterOptions.params 是跳转时传给目标页的数据
- 〔做法第 1 步〕module.json5 的 pages 指向的列表里，src 每一项是当前 Module 一个页面的路由信息，页面路径以当前 Module 的 src/main/ets 为基准
- 〔做法第 1 步〕router.pushUrl 的 url 写错或目标页面不存在时以错误码 100002（Uri error）失败，页面不跳转

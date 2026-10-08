# elevation 投影写入 ShadowOptions 时按 px 换算，并集中到一个按 elevation 推导的共享函数

ID：`lesson-d0aad947e26220fb43fa` · 版本：4 · 阶段：spec/execute/converge · 主题：[ui/theme/effects](index.md)

概要：elevation 阴影按 vp2px 换算并集中到共享函数

信号：`ShadowOptions`, `Modifier.shadow`, `vp2px`, `.shadow(`, `ShadowStyle`, `offsetX`

## 何时使用

规格提取阶段写阴影配方，以及界面实现、收敛阶段把 Modifier.shadow(elevation) 或 Surface 的 elevation 写成 ArkUI .shadow() 时

## 适用情境

源端以 dp 表示阴影高度；目标 ShadowOptions 的 radius/offsetX/offsetY 数值按 px 解释，而 width、padding 等长度属性默认是 vp。工程可能已有共享的 elevation→shadow 映射函数，个别页面也可能用预置 ShadowStyle 或字面值。

## 原因

“dp→vp 1:1”只适用于长度属性（SDK common.d.ts 注明 ShadowOptions 数值为 px）；把 dp 数值直写进 ShadowOptions，高密度屏上模糊只剩几分之一，阴影几乎不可见。偏差有两种来路：套用长度属性的换算规则，或写配方时 grep 只留了字段签名、过滤掉单位注释。预置 ShadowStyle 与源端高程没有对应关系，替代后既不随高程变化，也绕开了共享函数。

## 做法

1. radius、offsetX、offsetY 用 uiContext.vp2px(源 dp 值) 换算，把单位和换算写进公式本身，集中到一个按 elevation 推导的共享函数；各页面不另写与 elevation 无关的“视觉近似”常量，也不用预置 ShadowStyle 代替源端的具体高程。
2. 源端平台阴影由环境光和屏幕顶端主光两层组成，投影随元素位置变化，单层 ShadowOptions 只能近似：有源端截图时按多档高程实测校准共享函数的常量，没有时登记为需截图校准的视觉近似项，不在注释里写成等价映射。

## 可选检查

- 收敛后有疑问时检索 '.shadow('，确认全工程只剩共享函数一条通路，每个数值字段都经过换算。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [依赖 API 单位或默认行为时读声明紧邻注释](../../../arkts/api-signatures/lesson-f5cf8413ebea57f3b415.lesson.md)（共享 2 张卡）
- [派工必读清单覆盖语义来源，提速要求下也保留](../../../process/handoff-loss/lesson-8598e0af342dd5c8ba28.lesson.md)（共享 1 张卡）

来源支持：2 张卡 · 2 次迁移 · 1 个应用

## 来源（按需复核）

- [case-6aedeaac4c252c3c5626](../../../../../store/cases/case-6aedeaac4c252c3c5626/cb859fb4cd4eff0d54a717636ac7b7bcac5b5b0656eb9688d0f19721977a84b9.json) · 结论：diagnosis, rec-65b78b610f, rec-020a3810e1, rec-899b57936c
  卡片版本：`cb859fb4cd4eff0d54a717636ac7b7bcac5b5b0656eb9688d0f19721977a84b9`
- [case-75329cae60986f74dc43](../../../../../store/cases/case-75329cae60986f74dc43/03422478523b463e70feeccf65d3a54f73c2cf4463d4df454e234046c3cc04f1.json) · 结论：diagnosis, rec-0266f5b297, rec-5370b80b97, rec-541c329511
  卡片版本：`03422478523b463e70feeccf65d3a54f73c2cf4463d4df454e234046c3cc04f1`

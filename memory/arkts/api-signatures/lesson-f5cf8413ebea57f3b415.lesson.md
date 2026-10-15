# 依赖 API 的单位、默认行为或作用范围写契约或代码时，源端与目标端都读到声明注释或文档的语义说明，不以签名存在推定等价

ID：`lesson-f5cf8413ebea57f3b415` · 版本：6

[本主题](index.md)

## 何时使用

规格提取、实现或接线阶段，准备依赖某个 API（源端或目标端）的数值单位、默认是否占位、对子节点的作用、单行与多行排版语义写映射契约或代码时，例如 ShadowOptions 半径与偏移、hitTestBehavior 的 HitTestMode、Compose lineHeight、根 Navigation 标题栏是否占位、同名接口的不同重载

## 适用情境

当前疑点涉及数值单位（px 还是 vp）、默认是否占位、对子节点的作用、单行与多行的排版语义等；查询只返回同名签名、字段声明行或接口前言，或 grep 过滤掉了紧邻的注释行；或同名接口有多个重载（如按 Resource 对象与按数字 id 取资源字符串），查询只证明它们都存在。

## 例外与边界

- 当前输入已有适用版本下的明确规则或已成立实现时，直接复用，无需重复查证或补写证明材料。

## 原因

签名相同不等于语义相同：ShadowOptions 的 radius 与偏移单位是 px（注释写明），HitTestMode.Block 也会阻塞子节点，Compose lineHeight 与 ArkUI .lineHeight 的作用范围不同，根 Navigation 不设 title 时默认标题栏或工具栏仍可能占位，只看签名或凭记忆都会定错。grep 截取字段行时，单位说明常在紧邻的注释行里被过滤掉。源 API 的作用范围同样决定契约：只抄字面参数会丢掉源端实际的作用区域与度量。

## 做法

1. 只针对当前疑点，打开所用 API 或字段的声明及紧邻注释、所在接口的说明或交互映射参考的对应表；返回停在签名或前言时接着读相邻行，直到能回答该疑点，不必重读整个 SDK。
2. 写映射契约时同时读源 API 的作用区域与度量，写出它实际作用在哪块区域、按什么度量（例：Android TextView 自动字号作用在控件尺寸减内边距的内容区、按控件字体测量），不只写字面参数；API 形态留到实现期对目标 .d.ts。
3. 把查到的单位、作用范围或默认行为写进当前表达式和映射契约（如 ShadowOptions 的 radius: uiContext.vp2px(e)）；关键换算留一句依据即可。
4. 文档措辞仍不足以确定行为时，改用不依赖该行为的写法，或沿用已成立路径并在正常回报里标出具体未决点，不把推断写成等价。

## 可选检查

- 只有实现与声明仍有冲突时，局部对照实际用到的字段与结果。

来源支持：12 张卡 · 5 次迁移 · 4 个应用

## 来源（按需复核）

- [case-0e3ff99e6b2aa8afcfff](../../../store/cases/case-0e3ff99e6b2aa8afcfff/6cbb8aeffae0346c1d3aa2f31db6aa4d5ad2cfe987e616ee60fc181d992f940e.json) · 结论：recommendation:4
  卡片版本：`6cbb8aeffae0346c1d3aa2f31db6aa4d5ad2cfe987e616ee60fc181d992f940e`
- [case-30d42aa2ba7c8354db17](../../../store/cases/case-30d42aa2ba7c8354db17/caedcf037b4f51f56e370b09f5e18559d3a5abf76c513a88e701ad9ca342fe0f.json) · 结论：recommendation:1
  卡片版本：`caedcf037b4f51f56e370b09f5e18559d3a5abf76c513a88e701ad9ca342fe0f`
- [case-314b7ba3e75b6d6b3a9d](../../../store/cases/case-314b7ba3e75b6d6b3a9d/08fadc2330ff27e2cf5ad9e97831a12d5227c1325051da27dea7f806af0c0891.json) · 结论：diagnosis, recommendation:3
  卡片版本：`08fadc2330ff27e2cf5ad9e97831a12d5227c1325051da27dea7f806af0c0891`
- [case-4056358e68946ac061c6](../../../store/cases/case-4056358e68946ac061c6/5a37ff393ac488101441f9a3889af9b15392ce1ebfecf83f56931f1255d3bc75.json) · 结论：recommendation:1
  卡片版本：`5a37ff393ac488101441f9a3889af9b15392ce1ebfecf83f56931f1255d3bc75`
- [case-605ca2c835a2d8b2950f](../../../store/cases/case-605ca2c835a2d8b2950f/5885d2629daf3e1bd7b6e0ace40ac6b4389e87598667a069721cffe49353fd43.json) · 结论：recommendation:2
  卡片版本：`5885d2629daf3e1bd7b6e0ace40ac6b4389e87598667a069721cffe49353fd43`
- [case-6534af52334df8447e04](../../../store/cases/case-6534af52334df8447e04/56d6fa2d87fb62934a462b44a58ecab7d232cb683c20c6bf262b043cabd877c6.json) · 结论：recommendation:2, recommendation:1
  卡片版本：`56d6fa2d87fb62934a462b44a58ecab7d232cb683c20c6bf262b043cabd877c6`
- [case-6aedeaac4c252c3c5626](../../../store/cases/case-6aedeaac4c252c3c5626/cb859fb4cd4eff0d54a717636ac7b7bcac5b5b0656eb9688d0f19721977a84b9.json) · 结论：recommendation:1
  卡片版本：`cb859fb4cd4eff0d54a717636ac7b7bcac5b5b0656eb9688d0f19721977a84b9`
- [case-6b625c3cc6e754625383](../../../store/cases/case-6b625c3cc6e754625383/4c2ab9ddacab4aa86794ccbe9185ea14c6877b8e7be73cc108a7492e4e58ba55.json) · 结论：recommendation:2
  卡片版本：`4c2ab9ddacab4aa86794ccbe9185ea14c6877b8e7be73cc108a7492e4e58ba55`
- [case-75329cae60986f74dc43](../../../store/cases/case-75329cae60986f74dc43/03422478523b463e70feeccf65d3a54f73c2cf4463d4df454e234046c3cc04f1.json) · 结论：recommendation:1
  卡片版本：`03422478523b463e70feeccf65d3a54f73c2cf4463d4df454e234046c3cc04f1`
- [case-77c4d0c99ad4a6486b79](../../../store/cases/case-77c4d0c99ad4a6486b79/0c0854b7bb53f48c15425a1148239e8e459db928eb8f9600f5e5b1e1cc5042f4.json) · 结论：recommendation:2
  卡片版本：`0c0854b7bb53f48c15425a1148239e8e459db928eb8f9600f5e5b1e1cc5042f4`
- [case-77c6596fcdf362f9e832](../../../store/cases/case-77c6596fcdf362f9e832/c81c56fb66d294cfd767c2c43e5bcfb480ef9cccbdcfc212d5d607410c13675a.json) · 结论：recommendation:2
  卡片版本：`c81c56fb66d294cfd767c2c43e5bcfb480ef9cccbdcfc212d5d607410c13675a`
- [case-f4fef12b5d994df457b2](../../../store/cases/case-f4fef12b5d994df457b2/1df73908a2600045d97b85fa5e386b5b50972e141d1cd5505d5df882f5ebbad2.json) · 结论：recommendation:5
  卡片版本：`1df73908a2600045d97b85fa5e386b5b50972e141d1cd5505d5df882f5ebbad2`

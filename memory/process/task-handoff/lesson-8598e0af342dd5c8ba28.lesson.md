# 派工的必读清单、阅读顺序与对接清单要覆盖任务依赖的语义来源（框架约束、源工程路径、移交的验收条款），附加提速要求时也保留

ID：`lesson-8598e0af342dd5c8ba28` · 版本：6

[本主题](index.md)

## 何时使用

执行编排阶段，给页面转换、公共组件或收敛替换任务写派工，附加“效率纪律”、规定逐项“读源→立即写”的顺序，或列出要换成共享原语的对接点时；派发“对比源端还原某功能或页面”的实现任务时；维护共享踩坑参考、在切片之间移交职责时

## 适用情境

派工为提速限制阅读范围，或按组件清单规定阅读顺序；被写的组件依赖 Modifier 扩展、交互映射参考中的 API 语义表等外部定义；收敛任务要把页面私有写法替换成映射文档里的共享原语（阴影、排版等），并允许整文件重写。也包括并行派发对比与实现子代理，派工没写源工程路径与对应 Screen/ViewModel/Service。也包括某些框架约束只出现在某页注释、某个 skill 或移出方笔记里（一个组件只挂一个半模态、列表键须随实例变化、百分比宽度叠加外边距溢出、深色模式专项 skill、聚合器状态映射条款），接收方的写前输入里没有。

## 例外与边界

- 多个并行任务会写同一共享文件：按单一写者的经验指定作者

## 原因

被限制阅读的实现者会跳过 API 语义参考、凭记忆定稿；被依赖的源排在消费组件之后读，写组件时拿不到默认参数（如描边宽度），读到后也未必回头修正。对接清单只点名部分共享原语时，未点名的私有写法会在整文件重写中原样保留。已识别的约束不在接收方写前输入中时，接收方会按逐属性映射或惯例合理地写错，同一偏差在多页重现；职责移交只记在移出方笔记里，承接方拿不到验收条款。

## 做法

1. 附加效率要求时，仍把与本任务交互相关的语义参考（如命中测试控制表）列为必读。
2. 把被依赖的 Modifier 扩展等源文件排在消费它的组件之前，或要求随组件一起读取；允许后读时，要求读到后回查已写组件。
3. 派发收敛替换任务时，逐条列出映射文档里的全部共享原语及其对接点，要求执行者对读到的映射小节逐项对账、替换完成后再整文件重写。
4. 派发对比源端还原类任务时，先完成页面级行为对比（列表层级、模式状态、按钮可用条件）再派发实现；需要并行时，派工写明源工程路径和该功能的 Screen/ViewModel/Service 文件，要求实现者写前自行读取，派发后读到的对比结论与源端要点转交仍在运行的实现者。
5. 已识别的框架约束写进页面转换共享的踩坑参考或派工模板，不只留在某页注释里；负责事件处理、数据接线的切片同样拿到相关条目（如列表刷新条目），续跑或重试的 agent 重新加载完整参考，不只 grep 个别条目。
6. 转换器所用参考只有逐属性映射时，把布局组合规则（如 match_parent 加水平外边距不得直译）一并交付；涉及主题切换、系统栏、Canvas/Web 取色的切片把深色模式专项 skill 列入派工。
7. 源端某角色的职责移交给另一切片时，把对应验收条款写进承接切片的规格引用或派工，不只记在移出方笔记。

## 可选检查

- 收敛后有疑问时，检索原生属性（如 .shadow(）确认只剩共享函数调用。

来源支持：11 张卡 · 5 次迁移 · 4 个应用

## 来源（按需复核）

- [case-02008ba6db4e6a0ddfa2](../../../store/cases/case-02008ba6db4e6a0ddfa2/c4e9657f6da6da85435faa109fb5d920b0fe9b1560b66011aac636021cad5a18.json) · 结论：recommendation:4
  卡片版本：`c4e9657f6da6da85435faa109fb5d920b0fe9b1560b66011aac636021cad5a18`
- [case-30d42aa2ba7c8354db17](../../../store/cases/case-30d42aa2ba7c8354db17/caedcf037b4f51f56e370b09f5e18559d3a5abf76c513a88e701ad9ca342fe0f.json) · 结论：diagnosis, recommendation:4
  卡片版本：`caedcf037b4f51f56e370b09f5e18559d3a5abf76c513a88e701ad9ca342fe0f`
- [case-38718a95ad1839df7084](../../../store/cases/case-38718a95ad1839df7084/00eab77c139e8c3d0a58417a8df36dbebf5d067235aec37097d8ddd12e5bd8cd.json) · 结论：recommendation:2
  卡片版本：`00eab77c139e8c3d0a58417a8df36dbebf5d067235aec37097d8ddd12e5bd8cd`
- [case-40c445e1fb0a99ce0a72](../../../store/cases/case-40c445e1fb0a99ce0a72/2243b17f2f740e65ee1727d642a6aca74ef48f8bc924a7f9ccdcf12c9198d74b.json) · 结论：diagnosis, recommendation:5
  卡片版本：`2243b17f2f740e65ee1727d642a6aca74ef48f8bc924a7f9ccdcf12c9198d74b`
- [case-75329cae60986f74dc43](../../../store/cases/case-75329cae60986f74dc43/03422478523b463e70feeccf65d3a54f73c2cf4463d4df454e234046c3cc04f1.json) · 结论：diagnosis, recommendation:3
  卡片版本：`03422478523b463e70feeccf65d3a54f73c2cf4463d4df454e234046c3cc04f1`
- [case-be590c45de6e4195a7aa](../../../store/cases/case-be590c45de6e4195a7aa/8bd4ff591319a27aad91736ee43fe1cde1fd581f63d209f68e730ac2f406e5bb.json) · 结论：recommendation:4
  卡片版本：`8bd4ff591319a27aad91736ee43fe1cde1fd581f63d209f68e730ac2f406e5bb`
- [case-c1c7d598a9076a276e6a](../../../store/cases/case-c1c7d598a9076a276e6a/e08fcecfcb0ba66ded65b06bfca4e2fae61130f9835525a62f6e684c11cec824.json) · 结论：recommendation:3
  卡片版本：`e08fcecfcb0ba66ded65b06bfca4e2fae61130f9835525a62f6e684c11cec824`
- [case-c42ad6674b3abc0daece](../../../store/cases/case-c42ad6674b3abc0daece/ce2dd3a3dfa66b82469be871a9b2b7ca7f958335b5e9e2f52c6b4e12c126ac88.json) · 结论：diagnosis, recommendation:3
  卡片版本：`ce2dd3a3dfa66b82469be871a9b2b7ca7f958335b5e9e2f52c6b4e12c126ac88`
- [case-c4e5b6ca6da92a568d18](../../../store/cases/case-c4e5b6ca6da92a568d18/7fd836a3b3b3874e2f2f95df046b726804dddfab303ad8497ada8936a28e0940.json) · 结论：recommendation:5
  卡片版本：`7fd836a3b3b3874e2f2f95df046b726804dddfab303ad8497ada8936a28e0940`
- [case-c9559ed21540c28d4b53](../../../store/cases/case-c9559ed21540c28d4b53/79b4b26281e8d84401d25d862bdfd3bfea5d707c4a3e7c212b65fae1895abe56.json) · 结论：recommendation:3
  卡片版本：`79b4b26281e8d84401d25d862bdfd3bfea5d707c4a3e7c212b65fae1895abe56`
- [case-e1b1f9786e31a8d527cc](../../../store/cases/case-e1b1f9786e31a8d527cc/6698c0a41d8fb37c50b17d0fd1b124c9355c5b017e921353b28fbb208a63b460.json) · 结论：recommendation:6
  卡片版本：`6698c0a41d8fb37c50b17d0fd1b124c9355c5b017e921353b28fbb208a63b460`

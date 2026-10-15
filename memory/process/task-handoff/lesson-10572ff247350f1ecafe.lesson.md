# 子任务回报把工作指给其他负责方，或拆分、重派任务时，编排者把待接事项与原派工里的全局动作逐条写进负责方的派工

ID：`lesson-10572ff247350f1ecafe` · 版本：2

[本主题](index.md)

## 何时使用

执行编排阶段，收齐子任务返回、为下游切片或接线任务写派工，或拆分、重派子任务时；实现子代理运行期间编排者读到新的源端证据时

## 适用情境

子任务返回的 open_questions、风险项或文件头说明，把某项工作指给另一个阶段、切片或编排者本人（如返回键转发交给“入口装配或后续接线决定”，或回报某项“不在本段范围”）；上游交接把字体注册、主题模式同步、入口接线等全局动作指派给某个任务，该任务随后被拆分或重派；基础模块文档写着“由某负责方调用”“待闭环”“建议 P-ID”；派发页面接线任务时，页面规格里有导航关系与状态接口。也包括对比子代理只把结论回给编排者，或编排者自己读到源端界面与接口，而实现子代理仍在运行。

## 原因

全局动作与待接事项写在最初的派工、交接或回报文字里；拆分、重写派工时不逐条抄入，承接者就不知道它存在，而散文说明与报告条目会被编译和结构审计放行，结果是字体回退、深色不生效、返回键无人转发。运行中的实现者拿不到编排者后来读到的证据，回执仍按旧输入宣告完成。

## 做法

1. 收齐子任务返回后，把 open_questions、风险项里点名其他负责方的条目逐条分派：写进拥有相关文件的切片派工并写明调用点，或登记为待办，不随阶段推进丢弃；子任务回报某项“不在本段范围”时，当场指定承接任务，或在编排者自己装配入口时落地。
2. 拆分或重派任务前，把原派工与上游交接里指派给原任务的全局动作（注册、同步、入口接线等）和运行期要求（如深浅主题须可观察、由入口读取系统设置）列成清单，逐条写进新派工，注明落在哪个文件、哪个调用点；收尾前检索这些调用点，确认每一项都有真实调用。
3. 派发接线任务时，若上游说明要求该任务在壳页或调用点补转发，在派工里写明要实现的内容，或要求无法实现时上报阻塞；把对应页面规格的导航关系与状态接口一并交给接线者；派工带“其余不动”“禁碰某目录”之类写盘边界时，把这项移交列为例外，或把挡在边界外的延后项转成有归属的任务。
4. 上游文档里写着“由某负责方调用/待闭环/建议 P-ID”的条目，进入下一阶段前登记进占位表或转成源码移交标记，并写进该负责方的派工（写码者一侧的登记写法见 lesson-4f81eeea17b94190c2de）。
5. 并行运行中的实现者尚未拿到的对比结论或编排者新读到的源端证据，用 send_message 一类调用转发给它；转发未成功前不按子任务回执宣告完成。

来源支持：9 张卡 · 6 次迁移 · 6 个应用

## 来源（按需复核）

- [case-2880da61086b19aff2a4](../../../store/cases/case-2880da61086b19aff2a4/73345ae8b0a7d830ecb8996008d7c6c86c777fee1e5d5f115931faea4d82fc25.json) · 结论：recommendation:3, diagnosis
  卡片版本：`73345ae8b0a7d830ecb8996008d7c6c86c777fee1e5d5f115931faea4d82fc25`
- [case-2b9869554cf9027174a0](../../../store/cases/case-2b9869554cf9027174a0/399f7b12747efb0e2c5ee69d85083f67576d91c11b7c8f93adacb6d0713f92f6.json) · 结论：diagnosis, recommendation:3
  卡片版本：`399f7b12747efb0e2c5ee69d85083f67576d91c11b7c8f93adacb6d0713f92f6`
- [case-2c6857febfce92e5d5bc](../../../store/cases/case-2c6857febfce92e5d5bc/0de684fa8dfa58b7980ea4112552df78f4b747c3424b41d244d8715c38816ace.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`0de684fa8dfa58b7980ea4112552df78f4b747c3424b41d244d8715c38816ace`
- [case-38718a95ad1839df7084](../../../store/cases/case-38718a95ad1839df7084/00eab77c139e8c3d0a58417a8df36dbebf5d067235aec37097d8ddd12e5bd8cd.json) · 结论：diagnosis, recommendation:2
  卡片版本：`00eab77c139e8c3d0a58417a8df36dbebf5d067235aec37097d8ddd12e5bd8cd`
- [case-7b64dd743c1260eb910f](../../../store/cases/case-7b64dd743c1260eb910f/298567a76aee47097df89ce461b5d22ce36838d3b34afa1f21008596f2358535.json) · 结论：recommendation:4
  卡片版本：`298567a76aee47097df89ce461b5d22ce36838d3b34afa1f21008596f2358535`
- [case-9618601c4a21f2f18560](../../../store/cases/case-9618601c4a21f2f18560/870a2d98075a73dc88a2cfd3ac2fb801bc3d216cf1120c6f9583496d9f1c6941.json) · 结论：recommendation:3
  卡片版本：`870a2d98075a73dc88a2cfd3ac2fb801bc3d216cf1120c6f9583496d9f1c6941`
- [case-c9559ed21540c28d4b53](../../../store/cases/case-c9559ed21540c28d4b53/79b4b26281e8d84401d25d862bdfd3bfea5d707c4a3e7c212b65fae1895abe56.json) · 结论：diagnosis, recommendation:3
  卡片版本：`79b4b26281e8d84401d25d862bdfd3bfea5d707c4a3e7c212b65fae1895abe56`
- [case-cfcb1be64b70e328ad81](../../../store/cases/case-cfcb1be64b70e328ad81/3149ab3429330e943123e716dd39905b242a535966c5e16dffe17278714a0381.json) · 结论：diagnosis, recommendation:1
  卡片版本：`3149ab3429330e943123e716dd39905b242a535966c5e16dffe17278714a0381`
- [case-d9c2b75062eb57796ca2](../../../store/cases/case-d9c2b75062eb57796ca2/c0e0684d2567560ee8d44f49d9c8eb3a4d4b3cc9ba5d7380a8e25a3b0f7792e8.json) · 结论：recommendation:4
  卡片版本：`c0e0684d2567560ee8d44f49d9c8eb3a4d4b3cc9ba5d7380a8e25a3b0f7792e8`

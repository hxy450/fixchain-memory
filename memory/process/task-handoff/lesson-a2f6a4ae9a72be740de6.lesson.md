# “不确定”“待补资源”“无等价”“延期”“契约未确认”这类占位只登记输入确实缺值的情况：登记前查源码、SDK 与写入时刻的目录，能实现的当场实现

ID：`lesson-a2f6a4ae9a72be740de6` · 版本：4

[本主题](index.md)

## 何时使用

页面转换阶段决定是否登记 forward-ref-uncertain、resource-pending-asset 等占位，以及收口或验收阶段把这些占位改成 deferred 时；接线阶段决定尚未接通的页面动作是实现还是给出不可用提示时；把源端效果登记为“无等价/保留近似”，或派发对已登记近似项的复审时；收尾闭环处理指向本组或“集成期”的占位、准备按降级形态关单时

## 适用情境

工程提供多种占位类型（不确定值、待补资源、延期），页面规格置信度为 medium 或同名资源看似存在；源码和规格其实已给出行为或所需图形。也包括接线者给尚未接通的页面动作统一写 fail-loud 兜底（如“契约未确认，暂不可用”），而源端这些动作已有实现、目标工程也已有承担它们的共享组件。也包括实现者认为目标框架缺少对应能力（混合模式、端点渐变平铺等）而写入“无等价、保留近似”登记，复审派工又预写“保留”；或页面转换与资源迁移并行，转换者在资源复制完成前列目录看到空目录，就登记“资源未就绪”并改用降级。也包括写者只按对称方法名检索就把平台能力判为“无对等 API”，把可在本地实现的变换、自有端点引擎或页内权限链挂成依赖未建工件，以及收尾者为避开债务闸把占位改挂“集成期”“死码域披露”或按降级现状关单。

## 例外与边界

- 缺的确实是输入里没有的值，例如合成快照缺少尺寸、资源映射表里没有对应资产

## 原因

占位把能实现的工作挂成债务，后续阶段看到“已登记”就放过，直到验收门把 deferred 判成阻塞。来源两例：顶栏连续折叠在源码里写明，陷阱表也给了做法，转换者因页面置信度 medium 登记“不确定”；动画图标的资产存在，缺的是按状态选帧，转换者挂成“待补资源”。收口阶段两次改 resolve_by、标 deferred，都没有回看源码。另一应用中接线者读到源端把详情动作委托给共享详情弹窗、目标已有同名组件，仍把分享、附件、前序、添加后续、更多菜单统一改成“契约未确认”提示。“目标没有”常是没查 SDK；复审派工预写“保留”时后来者只会背书、不会复核。写入前看到的空目录也可能只是资源还在复制，沿用他人 pending 登记而不核触发条件，降级就一直保留到交付。改挂到不属于任何切片的延迟或“死码披露”后，债务闸放行，代码里的空桩、降级与 TODO 一直保留到交付。

## 做法

1. 登记前判断：缺的是输入里的值，还是实现工作？后者当场实现；确实做不到，在报告里写明缺哪一项（哪一帧、哪个值）。
2. 页面置信度 medium 不要求产出不确定标记；引用陷阱表条目时核对它给的修法与自己的实现一致。
3. 收口或验收阶段处理这类条目时先回看条目指向的源码与代码现状；能实现就实现，只有确需真机数据或依赖确在仓外（三方 SDK 或平台 API 缺失）时才改为 deferred。不把占位改挂到没有切片认领的“集成期”或“死码域披露”来消除债务闸，也不按降级现状翻为 resolved；已转换并注册路由的死码页，要么撤销转换与注册，要么按源码兑现页内占位。
4. 写 fail-loud 或不可用提示前逐项核对：源端该动作是否已有实现、目标端是否已有等价组件或服务；两者都有就接线复用；只有平台凭据等真实外部缺口才给阻断提示，并在提示和交接中写明具体缺口。
5. 登记“无等价”前在本地 SDK 的 .d.ts（含 hms/ets/kits）按能力语义检索：对应枚举、属性名、属性集合读取（如 getXxxProperties）、设置模块的键与候选模块文件，不只猜对称的 getter 名；把检索词与结论写进登记；同工程已有可行写法时直接沿用。
6. 写“资源未就绪、暂用降级”或沿用他人 pending 登记前，在写入时刻重新列出目标资源目录，或执行登记里的可机读触发条件，确认确实缺失。
7. 派发复审或切片工单时只给已登记条目与证据，不预写“保留”，要求执行者对照 SDK 与同工程已有实现复核后再裁决。

来源支持：14 张卡 · 4 次迁移 · 4 个应用

## 来源（按需复核）

- [case-0ac442a09e1e8ee36a8a](../../../store/cases/case-0ac442a09e1e8ee36a8a/a8ef5f4a3b6e86969bb09b0df9de25820f2b67887ac0349a98141071b3b6b276.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`a8ef5f4a3b6e86969bb09b0df9de25820f2b67887ac0349a98141071b3b6b276`
- [case-1cad884865343910ce02](../../../store/cases/case-1cad884865343910ce02/27369625dcbbe450f68beab2e162e179bde87573f0d20d5282655293b42e24d3.json) · 结论：recommendation:3
  卡片版本：`27369625dcbbe450f68beab2e162e179bde87573f0d20d5282655293b42e24d3`
- [case-265e1cc8347c261db79d](../../../store/cases/case-265e1cc8347c261db79d/125931927fbc468c3e5693050724034362006e87a40785f9580987d32edde5bb.json) · 结论：diagnosis, recommendation:2
  卡片版本：`125931927fbc468c3e5693050724034362006e87a40785f9580987d32edde5bb`
- [case-5235937ddd5c78dbe0ed](../../../store/cases/case-5235937ddd5c78dbe0ed/46e8691c9a380b7020a55b5bb495cfe4e5301c7d03dfaa4c5cfd4a2dac43ab17.json) · 结论：recommendation:3, recommendation:5
  卡片版本：`46e8691c9a380b7020a55b5bb495cfe4e5301c7d03dfaa4c5cfd4a2dac43ab17`
- [case-55c399941834500546bc](../../../store/cases/case-55c399941834500546bc/2ed24c92029a39c4d2dc7e81d018585ba69a1a2cb0e53cc2d7323021790566a2.json) · 结论：recommendation:3
  卡片版本：`2ed24c92029a39c4d2dc7e81d018585ba69a1a2cb0e53cc2d7323021790566a2`
- [case-583c797930b89c0d4e63](../../../store/cases/case-583c797930b89c0d4e63/f5953e9f12a3bcae8f4a8ae23194b2301733b2226bbed362e363b07da33b903c.json) · 结论：recommendation:4
  卡片版本：`f5953e9f12a3bcae8f4a8ae23194b2301733b2226bbed362e363b07da33b903c`
- [case-5c6be3ec08184086fd79](../../../store/cases/case-5c6be3ec08184086fd79/c810aaf2a57238a08e8f5f345b00a2df05d06d9887d763dc1d4de5f56ff633f0.json) · 结论：diagnosis, recommendation:1, recommendation:3
  卡片版本：`c810aaf2a57238a08e8f5f345b00a2df05d06d9887d763dc1d4de5f56ff633f0`
- [case-66f3c1649b7b5c4f38b5](../../../store/cases/case-66f3c1649b7b5c4f38b5/686410a72e498ff1fb1d9233686e5ebc690a444c3056d62bc78d50dbcb257140.json) · 结论：recommendation:3, recommendation:4
  卡片版本：`686410a72e498ff1fb1d9233686e5ebc690a444c3056d62bc78d50dbcb257140`
- [case-753b41488ff67ec1d068](../../../store/cases/case-753b41488ff67ec1d068/24570f598b1c5b1bdb181efddaac5a79a2aac2ad6e83f5f171a7107944d77842.json) · 结论：diagnosis, recommendation:3
  卡片版本：`24570f598b1c5b1bdb181efddaac5a79a2aac2ad6e83f5f171a7107944d77842`
- [case-75784c189c0578d026a6](../../../store/cases/case-75784c189c0578d026a6/86dd42e7e9d78e101a4bd803a4210cddbe07659a8deb38852f8201fe10a1d261.json) · 结论：recommendation:4
  卡片版本：`86dd42e7e9d78e101a4bd803a4210cddbe07659a8deb38852f8201fe10a1d261`
- [case-77e4e8b4e16c3fc8e030](../../../store/cases/case-77e4e8b4e16c3fc8e030/de5d2060d2228797992daa36c3c487459c5ec7e968bdca7f1d06ed589e393635.json) · 结论：recommendation:3
  卡片版本：`de5d2060d2228797992daa36c3c487459c5ec7e968bdca7f1d06ed589e393635`
- [case-cfcb1be64b70e328ad81](../../../store/cases/case-cfcb1be64b70e328ad81/3149ab3429330e943123e716dd39905b242a535966c5e16dffe17278714a0381.json) · 结论：recommendation:3
  卡片版本：`3149ab3429330e943123e716dd39905b242a535966c5e16dffe17278714a0381`
- [case-ddbf301e2e83a466c644](../../../store/cases/case-ddbf301e2e83a466c644/dab3bcf4ca202ab2876fe7261e1bd211d29a2f32dae0da3a88e1ed005df5fda9.json) · 结论：recommendation:1, recommendation:3
  卡片版本：`dab3bcf4ca202ab2876fe7261e1bd211d29a2f32dae0da3a88e1ed005df5fda9`
- [case-f4f67940ef03672d639c](../../../store/cases/case-f4f67940ef03672d639c/0c84d1476bf96ef042d71bcce5b94c7ae01ad2cf21e2004e85cd794b9ed5ca63.json) · 结论：recommendation:4
  卡片版本：`0c84d1476bf96ef042d71bcce5b94c7ae01ad2cf21e2004e85cd794b9ed5ca63`

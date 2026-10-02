# 规格或派工写法与写前读到的源码、主题或映射参考冲突或遗漏时，按源端语义实现并标注差异

ID：`lesson-7a065e8fe384b8c462cc` · 版本：9

[本主题](index.md)

## 何时使用

页面或数据层实现阶段，规格或派工给出的容器、样式、类型写法、槽位或验收条目与写前读到的源码、主题或映射参考不一致，或验收条目没有列出源码里可见的行为时；重构或模块迁移阶段，规格清单要求改变已与源端一致的现有行为时

## 适用情境

实现者同时读到规格或派工与源布局、源码、主题文件、映射参考或 SDK 声明，规格的具体写法（含验收条目里的列表范围、过滤条件、容器类型、要求新建的槽位、所引源布局、列举顺序、启动去向）与源端可观察行为或参考映射不符，或验收条目漏掉了源码对展示内容的加工；规格对该处只有概括性理由或没有提及。也包括规格的 gap 条目写着“源端是 X、规格要求 Y、按规格实现”，而现有目标实现已与源端一致。派工声明“规格为权威”、规格条款（取值、方向、数量等）与源码运行语义矛盾而已有实现恰好符合源码时同样适用。也包括巡检或修复单的修法与决策台账总则（如核心流程必须真实可用）、工程硬性条款或源端行为冲突，修复者写前同时读到了双方。

## 例外与边界

- 规格或决策记录（如 decision ledger）对该差异写明了有意取舍（例如只在成功后写缓存、先授权再定位），此时按该决策实现，并在报告里写明与源码的差异

## 原因

规格、派工和映射参考是对源端行为的二手概括，可能写错容器、取值范围或顺序，也可能漏掉可见行为。实现者已读到相反输入，却以符合规格或验收项未列为由保留差异，就会把概括错误落实到代码；重构时同样可能把已正确的行为改偏。这里的偏差是转述错误覆盖已确认的源端语义，而非明确批准的行为取舍。

## 做法

1. 写码前对冲突点逐一取舍：规格只有概括性理由时，以源端可观察行为为准实现；涉及 API 签名的，以本地 SDK 声明为准。验收条目标注了源码出处时，打开该出处核对。
2. 源码里有、验收条目没写的可见行为，不能据此判定可删：按源码实现；做不了就登记占位，并在报告未决项里写明降级。
3. 在转换或迁移报告里列出与规格不同的每一处及依据，供规格阶段回改；不要为了与规格一致而删掉已确认的源端语义，也不要在注释写“交验证复核”后仍按规格值改掉已符合源码的实现。
4. 重构或模块迁移默认保持现有行为：现有实现已与源端一致、只有规格清单不同时，改规格或登记决策，不按清单改代码行为；真机验证也按源端期望断言，不把“符合当前规格”当作通过依据。
5. 执行巡检或修复单时同样对照台账与工程硬性条款：修复单把某项失败语义扩大成阻断核心功能等与台账冲突的要求时，按台账与源端行为实现，并在回执里标出与修复单的分歧。

来源支持：14 张卡 · 8 次迁移 · 8 个应用

## 来源（按需复核）

- [case-1d6dca36cb9c3cec5d87](../../../store/cases/case-1d6dca36cb9c3cec5d87/1e37801e16b9b0ef1a39188c29ab362ac81d454a0e8e3565f3947e635a917c8a.json) · 结论：diagnosis, recommendation:2
  卡片版本：`1e37801e16b9b0ef1a39188c29ab362ac81d454a0e8e3565f3947e635a917c8a`
- [case-356f707ace6e648548be](../../../store/cases/case-356f707ace6e648548be/c4c0e0e3fcf9bc2ed30570f839c47fb3ee15ecd05d7433d84550aade9e272c8d.json) · 结论：recommendation:4
  卡片版本：`c4c0e0e3fcf9bc2ed30570f839c47fb3ee15ecd05d7433d84550aade9e272c8d`
- [case-3db1068ed462e12cf813](../../../store/cases/case-3db1068ed462e12cf813/e619d9487fd9bdbba6d0959e7b2935f08c667fed9eb9dc3d02e929ea5fc2076a.json) · 结论：recommendation:4
  卡片版本：`e619d9487fd9bdbba6d0959e7b2935f08c667fed9eb9dc3d02e929ea5fc2076a`
- [case-6448a485599bfc0740c6](../../../store/cases/case-6448a485599bfc0740c6/ee79f91fda0232a915c1fd976889b9b074c5a5ebef6177e7b7704b4c30211b79.json) · 结论：recommendation:3
  卡片版本：`ee79f91fda0232a915c1fd976889b9b074c5a5ebef6177e7b7704b4c30211b79`
- [case-64d73b23ce87a7bad738](../../../store/cases/case-64d73b23ce87a7bad738/8fe55754fa54a93eeaf56091bece36132f8bbf77e051383d870b13487a898e49.json) · 结论：diagnosis, recommendation:1, recommendation:3, recommendation:4
  卡片版本：`8fe55754fa54a93eeaf56091bece36132f8bbf77e051383d870b13487a898e49`
- [case-7f41c5604c3a5213023b](../../../store/cases/case-7f41c5604c3a5213023b/4242659d6c555274f4b22e2a7d309bf85bb1c658b28e7509473a012ac96234c8.json) · 结论：diagnosis, recommendation:3
  卡片版本：`4242659d6c555274f4b22e2a7d309bf85bb1c658b28e7509473a012ac96234c8`
- [case-8128c57ee5fb2e4f49d1](../../../store/cases/case-8128c57ee5fb2e4f49d1/d0184e877064d037eceb8bc968cb0949b5d0bffb239f02ec1d1a93bf7a391713.json) · 结论：diagnosis, recommendation:2
  卡片版本：`d0184e877064d037eceb8bc968cb0949b5d0bffb239f02ec1d1a93bf7a391713`
- [case-8c249997059a2524ea7b](../../../store/cases/case-8c249997059a2524ea7b/921750461c1e7e278c419ca26c21b17048d692c94b180c54164c66f94aafa6e6.json) · 结论：recommendation:3
  卡片版本：`921750461c1e7e278c419ca26c21b17048d692c94b180c54164c66f94aafa6e6`
- [case-8fced432ea0fe7c8b86f](../../../store/cases/case-8fced432ea0fe7c8b86f/b4353b2e8b37ffe082eef91d15ac512e601071bb1ab5aaec8c56c4904d0256e7.json) · 结论：recommendation:2
  卡片版本：`b4353b2e8b37ffe082eef91d15ac512e601071bb1ab5aaec8c56c4904d0256e7`
- [case-97a40a9d2dce65dc9f9c](../../../store/cases/case-97a40a9d2dce65dc9f9c/6f204ffd524b55f7ea8cef5e4a2e75cc8330004f202fd635570857c43cef5a2a.json) · 结论：diagnosis, recommendation:3
  卡片版本：`6f204ffd524b55f7ea8cef5e4a2e75cc8330004f202fd635570857c43cef5a2a`
- [case-b2793695ef65617c820a](../../../store/cases/case-b2793695ef65617c820a/9c30f15ba64082b90317b9cb20aa187c32cf5f93197443b2a9a78fe723ec3a47.json) · 结论：diagnosis, recommendation:4
  卡片版本：`9c30f15ba64082b90317b9cb20aa187c32cf5f93197443b2a9a78fe723ec3a47`
- [case-fa7bbda457517260efc4](../../../store/cases/case-fa7bbda457517260efc4/58d73cfa31553fee929796eb72c6f37fc2faba952a2e2f334aa420b8f0325b08.json) · 结论：recommendation:2
  卡片版本：`58d73cfa31553fee929796eb72c6f37fc2faba952a2e2f334aa420b8f0325b08`
- [case-fe9e7a0905bfe755e601](../../../store/cases/case-fe9e7a0905bfe755e601/e5e2e555edf9f128209192063835fa2e7691b3363f56bb34b6d3e0a21b7fb43a.json) · 结论：recommendation:3
  卡片版本：`e5e2e555edf9f128209192063835fa2e7691b3363f56bb34b6d3e0a21b7fb43a`
- [case-ff24fb8ea8e66a1cadd5](../../../store/cases/case-ff24fb8ea8e66a1cadd5/0f61ad0da67f3c08fc31506fea75dcac3fc3a6636c4a9df5d76a7e4d3a93830c.json) · 结论：diagnosis
  卡片版本：`0f61ad0da67f3c08fc31506fea75dcac3fc3a6636c4a9df5d76a7e4d3a93830c`

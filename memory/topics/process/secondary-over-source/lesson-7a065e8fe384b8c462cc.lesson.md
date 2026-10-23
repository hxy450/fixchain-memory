# 规格或派工与写前读到的源码、主题或映射参考冲突或遗漏时，按源端可观察行为实现并回报规格分歧；只有决策台账中带决策 ID 的取舍才例外，source-notes 登记与转述不算批准

ID：`lesson-7a065e8fe384b8c462cc` · 版本：16 · 阶段：execute/repair · 主题：[process/secondary-over-source](index.md)

概要：规格与源码冲突按源实现，例外只认决策 ID

信号：`decision_ref`, `decision_gaps`, `source-notes`, `PD-`, `HARD`, `.d.ts`

## 何时使用

页面或数据层实现阶段，规格或派工给出的容器、样式、类型写法、槽位或验收条目与写前读到的源码、主题或映射参考不一致，或验收条目没有列出源码里可见的行为时；重构或模块迁移阶段，规格清单要求改变已与源端一致的现有行为时

## 适用情境

实现者同时读到规格或派工与源布局、源码、主题文件、映射参考或 SDK 声明，规格的具体写法（含验收条目里的列表范围、过滤条件、容器类型、要求新建的槽位、所引源布局、列举顺序、启动去向）与源端可观察行为或参考映射不符，或验收条目漏掉了源码对展示内容的加工；规格对该处只有概括性理由或没有提及。也包括规格的 gap 条目写着“源端是 X、规格要求 Y、按规格实现”，而现有目标实现已与源端一致。派工声明“规格为权威”、规格条款（取值、方向、数量等）与源码运行语义矛盾而已有实现恰好符合源码时同样适用。也包括巡检或修复单的修法与决策台账总则（如核心流程必须真实可用）、工程硬性条款或源端行为冲突，修复者写前同时读到了双方。 也包括上游审计或规格写入了源码没有的防护属性（如“有界去重队列”），或摘要漏写源码里的分支（手势专用的动画时长、一次性引导），而实现者写前手里同时有源码。

## 例外与边界

- 决策台账中有带决策 ID（如 D-、PD-）的条目明确声明与源端不同的取舍（验收条目带决策锚点或 decision_ref），此时按该决策实现，并在报告里写明与源码的差异；规格或派工里的转述值、锚点仍指向源码而 decision_ref 为空的条目不算决策

## 原因

规格、派工和映射参考是对源端行为的二手概括，可能写错容器、取值范围或顺序，也可能漏掉可见行为。实现者已读到相反输入，却以符合规格或验收项未列为由保留差异，就会把概括错误落实到代码；重构时同样可能把已正确的行为改偏。这里的偏差是转述错误覆盖已确认的源端语义，而非明确批准的行为取舍。例外条款若只写“规格或决策记录写明取舍”，转述成另一个字面值的验收条目也会被当成决策；“标注差异”又会被读成目标相对源端的收敛写进笔记即可保留。

## 做法

1. 写码前对冲突点逐一取舍：先查决策台账有无带决策 ID 的条目覆盖该差异；没有就以源端可观察行为为准实现（规格只有概括性理由，或把源资源值转述成另一个字面值、锚点仍是源码时同样如此）；涉及 API 签名的以本地 SDK 声明为准。验收条目标注了源码出处时，打开该出处核对。
2. 源码里有、验收条目没写的可见行为，不能据此判定可删：按源码实现；做不了就登记占位，并在报告未决项里写明降级。
3. 在转换或迁移报告里列出与规格不同的每一处及依据，供规格阶段回改；不要为了与规格一致而删掉已确认的源端语义，也不要在注释写“交验证复核”后仍按规格值改掉已符合源码的实现。
4. 重构或模块迁移默认保持现有行为：现有实现已与源端一致、只有规格清单不同时，改规格或登记决策，不按清单改代码行为；真机验证也按源端期望断言，不把“符合当前规格”当作通过依据。
5. 执行巡检或修复单时同样对照台账与工程硬性条款：修复单把某项失败语义扩大成阻断核心功能等与台账冲突的要求时，按台账与源端行为实现，并在回执里标出与修复单的分歧。
6. 上游审计或规格加入源码没有的属性（去重、条数上限、点击清空）或漏写源码分支时，同样以源码为准实现，在交接里写明冲突；确需目标侧保护的另列为适配策略，说明对可见结果的影响后交负责方确认。
7. “标注差异”只记录规格与源码的分歧，实现仍按源端；目标相对源端少了可见行为（弹窗个数、回调次数、Toast）时不属于可标注的差异，要么按源端实现，要么作为待批决策写入台账或 handback 的 decision_gaps 等待裁决，source-notes 与注释里的登记不算批准。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [验收条目实读源码段落，照抄比较符并给边界样例](../enumeration-gaps/lesson-08854573a81a9fa03746.lesson.md)（共享 4 张卡）
- [跨文件补实现的功能登记带负责方与验证的移交项](../handoff-loss/lesson-4f81eeea17b94190c2de.lesson.md)（共享 3 张卡）
- [源端可观察缺陷照迁并核次数，修正走待批决策](../unapproved-deviation/lesson-14411595fd9ac1e17683.lesson.md)（共享 2 张卡）
- [必读 skill 与源码逐份读全，截断即重读再写码](../unloaded-input/lesson-42df1ac4d4030421da34.lesson.md)（共享 2 张卡）
- [PowerShell 读文件带 UTF8 编码，乱码视为未读](../unloaded-input/lesson-6a3a7f46c8fec282affa.lesson.md)（共享 2 张卡）

来源支持：33 张卡 · 已知 15 次迁移（部分未记录） · 已知 14 个应用（部分未记录）

## 来源（按需复核）

- [case-0848ab137044cb92d1bc](../../../../store/cases/case-0848ab137044cb92d1bc/1b8dbd30951aec40912fda717800da9383cdc52429f479cbae2d27c1fd708e37.json) · 结论：diagnosis
  卡片版本：`1b8dbd30951aec40912fda717800da9383cdc52429f479cbae2d27c1fd708e37`
- [case-0a19acd6cfea1aafecbe](../../../../store/cases/case-0a19acd6cfea1aafecbe/589a48e8446be4ea4c5d6a58af60ae396336c5d09a583600cda3be920a1e071a.json) · 结论：rec-82028b3e32
  卡片版本：`589a48e8446be4ea4c5d6a58af60ae396336c5d09a583600cda3be920a1e071a`
- [case-1a09dd649093f650a6fc](../../../../store/cases/case-1a09dd649093f650a6fc/da04b374b7092b19b66477caa7b72bf7555cde232a69d7d65bab1fe080a2a458.json) · 结论：diagnosis
  卡片版本：`da04b374b7092b19b66477caa7b72bf7555cde232a69d7d65bab1fe080a2a458`
- [case-1d6dca36cb9c3cec5d87](../../../../store/cases/case-1d6dca36cb9c3cec5d87/1e37801e16b9b0ef1a39188c29ab362ac81d454a0e8e3565f3947e635a917c8a.json) · 结论：diagnosis, rec-aa4f54b2ad
  卡片版本：`1e37801e16b9b0ef1a39188c29ab362ac81d454a0e8e3565f3947e635a917c8a`
- [case-29fdf1fe3faadb5933b9](../../../../store/cases/case-29fdf1fe3faadb5933b9/7e89a2a29280e57f4b1930d3be3e5cf0ef1d7b50676e2d240862c6794865b214.json) · 结论：rec-35d099069b
  卡片版本：`7e89a2a29280e57f4b1930d3be3e5cf0ef1d7b50676e2d240862c6794865b214`
- [case-3094b57f19bdd601c03e](../../../../store/cases/case-3094b57f19bdd601c03e/9d34746173f7a47aae89f921c5b451e93ee5312a94b4f1bd66a04f4d6df54dff.json) · 结论：rec-c52506bf6c
  卡片版本：`9d34746173f7a47aae89f921c5b451e93ee5312a94b4f1bd66a04f4d6df54dff`
- [case-3393a7b63a1c499d3e05](../../../../store/cases/case-3393a7b63a1c499d3e05/087ad61eaf4cd66f5dd27160d6f41eb70eb9c6fde92f045fd1fa60037f6c32c9.json) · 结论：diagnosis, rec-a5fbd8bdac
  卡片版本：`087ad61eaf4cd66f5dd27160d6f41eb70eb9c6fde92f045fd1fa60037f6c32c9`
- [case-34903093a988aad52061](../../../../store/cases/case-34903093a988aad52061/e127c825ec9e70a3c6237159da0b285cf7d81483112e4a883a38d41762f5a5aa.json) · 结论：diagnosis, rec-f8dd673671
  卡片版本：`e127c825ec9e70a3c6237159da0b285cf7d81483112e4a883a38d41762f5a5aa`
- [case-356f707ace6e648548be](../../../../store/cases/case-356f707ace6e648548be/c4c0e0e3fcf9bc2ed30570f839c47fb3ee15ecd05d7433d84550aade9e272c8d.json) · 结论：rec-199c188498
  卡片版本：`c4c0e0e3fcf9bc2ed30570f839c47fb3ee15ecd05d7433d84550aade9e272c8d`
- [case-3db1068ed462e12cf813](../../../../store/cases/case-3db1068ed462e12cf813/e619d9487fd9bdbba6d0959e7b2935f08c667fed9eb9dc3d02e929ea5fc2076a.json) · 结论：rec-c7d09a8747
  卡片版本：`e619d9487fd9bdbba6d0959e7b2935f08c667fed9eb9dc3d02e929ea5fc2076a`
- [case-58b7b9c32dd320dca714](../../../../store/cases/case-58b7b9c32dd320dca714/72151b4cd7d105de53553def5a3b53c4a276f1eee7ce96418d386e3f5f67c0ca.json) · 结论：diagnosis, rec-f02fe7a002
  卡片版本：`72151b4cd7d105de53553def5a3b53c4a276f1eee7ce96418d386e3f5f67c0ca`
- [case-6448a485599bfc0740c6](../../../../store/cases/case-6448a485599bfc0740c6/ee79f91fda0232a915c1fd976889b9b074c5a5ebef6177e7b7704b4c30211b79.json) · 结论：rec-1d95ca19a6
  卡片版本：`ee79f91fda0232a915c1fd976889b9b074c5a5ebef6177e7b7704b4c30211b79`
- [case-64d73b23ce87a7bad738](../../../../store/cases/case-64d73b23ce87a7bad738/8fe55754fa54a93eeaf56091bece36132f8bbf77e051383d870b13487a898e49.json) · 结论：diagnosis, rec-51e4d02c22, rec-cba017f0c9, rec-0a65112108
  卡片版本：`8fe55754fa54a93eeaf56091bece36132f8bbf77e051383d870b13487a898e49`
- [case-730269321014e7e1d765](../../../../store/cases/case-730269321014e7e1d765/d62d1ca408ead4c6087ee8493ffc6be944e20a88c5230ed7af8f16298d439621.json) · 结论：rec-c66cf2c5a0
  卡片版本：`d62d1ca408ead4c6087ee8493ffc6be944e20a88c5230ed7af8f16298d439621`
- [case-7c2d5eb3b8d385b5c7b7](../../../../store/cases/case-7c2d5eb3b8d385b5c7b7/4fe95717497af6c41c82096cc4afc4df7f1c2ba10ecd54294c53c633b1712a95.json) · 结论：diagnosis, rec-57bb983e73
  卡片版本：`4fe95717497af6c41c82096cc4afc4df7f1c2ba10ecd54294c53c633b1712a95`
- [case-7e6984a7fa6d5845737b](../../../../store/cases/case-7e6984a7fa6d5845737b/28061d97667de8051e1a704ca4104b16d7db6a03989478ec6a0298430dae5dba.json) · 结论：diagnosis
  卡片版本：`28061d97667de8051e1a704ca4104b16d7db6a03989478ec6a0298430dae5dba`
- [case-7f41c5604c3a5213023b](../../../../store/cases/case-7f41c5604c3a5213023b/4242659d6c555274f4b22e2a7d309bf85bb1c658b28e7509473a012ac96234c8.json) · 结论：diagnosis, rec-d7f17a4760
  卡片版本：`4242659d6c555274f4b22e2a7d309bf85bb1c658b28e7509473a012ac96234c8`
- [case-8128c57ee5fb2e4f49d1](../../../../store/cases/case-8128c57ee5fb2e4f49d1/d0184e877064d037eceb8bc968cb0949b5d0bffb239f02ec1d1a93bf7a391713.json) · 结论：diagnosis, rec-cae120cfb5
  卡片版本：`d0184e877064d037eceb8bc968cb0949b5d0bffb239f02ec1d1a93bf7a391713`
- [case-8572b9913886046a4b8f](../../../../store/cases/case-8572b9913886046a4b8f/4309c5ccef8db0cff0db4cc32eeff53d37f8381442971e99affa07e1dbd17047.json) · 结论：rec-2421da5615
  卡片版本：`4309c5ccef8db0cff0db4cc32eeff53d37f8381442971e99affa07e1dbd17047`
- [case-8c249997059a2524ea7b](../../../../store/cases/case-8c249997059a2524ea7b/921750461c1e7e278c419ca26c21b17048d692c94b180c54164c66f94aafa6e6.json) · 结论：rec-1b0004dc45
  卡片版本：`921750461c1e7e278c419ca26c21b17048d692c94b180c54164c66f94aafa6e6`
- [case-8dd5c1f1f269d142cc22](../../../../store/cases/case-8dd5c1f1f269d142cc22/20e8fe0eb12d923dd2187f8efe7cbc824971502cc6456d7985b1f26b5e5e94d9.json) · 结论：diagnosis
  卡片版本：`20e8fe0eb12d923dd2187f8efe7cbc824971502cc6456d7985b1f26b5e5e94d9`
- [case-8fced432ea0fe7c8b86f](../../../../store/cases/case-8fced432ea0fe7c8b86f/b4353b2e8b37ffe082eef91d15ac512e601071bb1ab5aaec8c56c4904d0256e7.json) · 结论：rec-e4438f67d5
  卡片版本：`b4353b2e8b37ffe082eef91d15ac512e601071bb1ab5aaec8c56c4904d0256e7`
- [case-91084f18203ecc5e7036](../../../../store/cases/case-91084f18203ecc5e7036/b2ef3d93c321f92d42c3adeb2614a39fc4a1d58051f93808ce0ad907fbc2e561.json) · 结论：rec-1a38060fff
  卡片版本：`b2ef3d93c321f92d42c3adeb2614a39fc4a1d58051f93808ce0ad907fbc2e561`
- [case-9720ed67e580c21dbd65](../../../../store/cases/case-9720ed67e580c21dbd65/e28f20a327f221aadfca37acb42f61db9e173a49a49fc0416d970ee8aeafb602.json) · 结论：rec-be8e730b62
  卡片版本：`e28f20a327f221aadfca37acb42f61db9e173a49a49fc0416d970ee8aeafb602`
- [case-97a40a9d2dce65dc9f9c](../../../../store/cases/case-97a40a9d2dce65dc9f9c/6f204ffd524b55f7ea8cef5e4a2e75cc8330004f202fd635570857c43cef5a2a.json) · 结论：diagnosis, rec-e645901bde
  卡片版本：`6f204ffd524b55f7ea8cef5e4a2e75cc8330004f202fd635570857c43cef5a2a`
- [case-9e50f3aa8db41be6d2fe](../../../../store/cases/case-9e50f3aa8db41be6d2fe/3d6143319a7bdfdbada20047728ad910934b06a242c61e2977d6a694908b4125.json) · 结论：diagnosis, rec-1c647a9ce8
  卡片版本：`3d6143319a7bdfdbada20047728ad910934b06a242c61e2977d6a694908b4125`
- [case-b2793695ef65617c820a](../../../../store/cases/case-b2793695ef65617c820a/9c30f15ba64082b90317b9cb20aa187c32cf5f93197443b2a9a78fe723ec3a47.json) · 结论：diagnosis, rec-7c53036290
  卡片版本：`9c30f15ba64082b90317b9cb20aa187c32cf5f93197443b2a9a78fe723ec3a47`
- [case-e74edb1116e46accfed6](../../../../store/cases/case-e74edb1116e46accfed6/e6d7581e5fabaf53a8b0e8ccc81556c84b10d557f6b636d3cc4ac2e4bba2d0c6.json) · 结论：rec-ff763eab8d, rec-2f7c207238
  卡片版本：`e6d7581e5fabaf53a8b0e8ccc81556c84b10d557f6b636d3cc4ac2e4bba2d0c6`
- [case-efe142b20bd2193d99da](../../../../store/cases/case-efe142b20bd2193d99da/12f8b12ad4e862daeac4fc39bfd929a98c7f6b9de58a944ede2dda9e25edcf1a.json) · 结论：rec-4eff9b8904
  卡片版本：`12f8b12ad4e862daeac4fc39bfd929a98c7f6b9de58a944ede2dda9e25edcf1a`
- [case-fa7bbda457517260efc4](../../../../store/cases/case-fa7bbda457517260efc4/58d73cfa31553fee929796eb72c6f37fc2faba952a2e2f334aa420b8f0325b08.json) · 结论：rec-174ea1344c
  卡片版本：`58d73cfa31553fee929796eb72c6f37fc2faba952a2e2f334aa420b8f0325b08`
- [case-fb9e44071c44d06a6c71](../../../../store/cases/case-fb9e44071c44d06a6c71/bf5d6bb212ef911888c7191fcdb2bb9477ac016ab3189fa909d1117ecde2f69b.json) · 结论：diagnosis
  卡片版本：`bf5d6bb212ef911888c7191fcdb2bb9477ac016ab3189fa909d1117ecde2f69b`
- [case-fe9e7a0905bfe755e601](../../../../store/cases/case-fe9e7a0905bfe755e601/e5e2e555edf9f128209192063835fa2e7691b3363f56bb34b6d3e0a21b7fb43a.json) · 结论：rec-0e7847c9f5
  卡片版本：`e5e2e555edf9f128209192063835fa2e7691b3363f56bb34b6d3e0a21b7fb43a`
- [case-ff24fb8ea8e66a1cadd5](../../../../store/cases/case-ff24fb8ea8e66a1cadd5/0f61ad0da67f3c08fc31506fea75dcac3fc3a6636c4a9df5d76a7e4d3a93830c.json) · 结论：diagnosis
  卡片版本：`0f61ad0da67f3c08fc31506fea75dcac3fc3a6636c4a9df5d76a7e4d3a93830c`

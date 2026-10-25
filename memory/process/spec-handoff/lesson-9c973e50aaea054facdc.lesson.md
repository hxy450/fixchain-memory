# 平台差异只收敛确实做不到的那一步：写“无对等”前查证并记录，替代方案只作用于源端同一路径，其余出口、分支与回退照源端保留

ID：`lesson-9c973e50aaea054facdc` · 版本：5

[本主题](index.md)

## 何时使用

规格提取与计划决策阶段，为源端平台专有能力（系统派发入口、商店跳转、系统设置深链、跨应用拉起、设备能力探测、运行时开关、画中画等系统窗口能力、系统取色、后台执行与通知动作），或目标没有现成组件的视觉与交互效果，登记平台差异、skip 或“已批准不可用”时；实现阶段消费这类差异决策时

## 适用情境

源端某条链路里只有个别步骤在目标平台确实做不到（如第三方不能运行时启停 skill、查询他包安装与运行状态），规格或台账却把整条入口判为“无对等”、把按钮出口改成说明文案、把不同探测结果合并成一个分支，或把替代开关接到源开关不影响的路径；计划汇总行把只批给少数能力的降级泛化到其他能力；实现者再把差异决策扩展到决策未列明的行为（如整段富文本链接都不实现）。“已查证”的说法可能没有对应的查询记录，或依据只是本地参考文件检索无命中、凭记忆断言。也包括目标只是没有现成组件或同名 API、可用滚动回调或 Canvas/Path 等通用能力组合实现的效果，被写成“简化为固定形态”；源码自带版本门槛与“不支持时回退”分支的能力被整体删除；源端检测手段在目标没有同名对应，被判定的状态却可以观察；子代理回执标为“存疑”的推断，或上游 skip-list 里的一句“无 API”，被下游升级为定论或改写成“d.ts 无对应条款”的依据。

## 例外与边界

- 决策记录明确批准了更大范围的收敛，并写明理由与用户可见影响

## 原因

“不能动态禁用”推不出“整条入口无对等”，“不能查询他包状态”推不出“不需要商店跳转”，“检测手段没有同名 API”推不出“行为删除”，“没有现成组件或同名 API”也推不出“只能简化”；差异范围一旦写大，下游会照单删掉源端仍可实现的出口、分支和回退，或把开关接到错误路径（关掉开关后前台功能也失效）。未执行的查证、子代理标为存疑的推断和汇总行里的泛化，经过转述都会被后续阶段当作已批准事实。来源中一个应用三处如此：清单声明的贴卡拉起入口被判为无对等、自启动开关改成了前台派发闸门；商店、设置深链与拉起他应用的出口被收敛为说明文本，“有 NFC 无 MFC”与“无 NFC”合并成同一分支；只涉及外跳出口的差异被扩大成正文链接都不实现。另一应用的计划汇总行把仅限认证、广告、微信的降级写成“地图执行已批准不可用”。

## 做法

1. 平台差异只收敛做不到的那一步（如他包状态恒为未知），源端按钮出口与回退链原样保留为“尝试 + 失败回退”（如 market:// 失败转 https 网页、设置子页失败退设置首页、拉起失败静默）；源码自带版本门槛或“不支持时回退”分支的能力，映射为“能力探测 + 原回退”，相关设置项的可用状态绑定探测结果。
2. 写“无对等/HARD-DIV/已查证”前，实际查项目 SDK 的 d.ts（ets/api、hms/ets/api 与 kits 导出，按能力关键词检索）、平台 skills 与能力文档，以及工程内现有的 startAbility、viewData 用法；把检索词、命中模块及其 @since、@deprecated、@systemapi、@permission 标注写进映射行。只检索了本地参考文档、映射表或凭记忆得出的“没有条目”，记为未查证，不升级为裁剪、HARD-DIV 或替代形态（例：固定桌面快捷方式、geo: 隐式拉起、整应用重启，在 API 24 SDK 中分别有 productViewManager.requestNewPinShortcut、bundleManager.canOpenLink、ApplicationContext.restartApp）。查不到就登记待定、交决策关口，不引用未执行的查证。只命中已弃用、仅系统可用或需权限的接口时，在决策中写出风险、失败回退与真机验证项，供审批在“降级”与“该接口 + 回退”之间选择，不写成无对等。决策关口收口时核对依据真实存在，并与同类裁决保持一致。
3. 目标只是没有现成组件或同名 API 时，先核对能否用通用能力组合实现（滚动回调加高度动画、Canvas/Path 自绘与动画、锚点加纯计算）；能实现就写成实现项并附源端参数，不登记平台差异。源端判定手段没有同名对应时，先写出用户可观察的条件与效果，再找目标上能观察到同一状态的信号。
4. 子代理回执标为“存疑/待定夺”的平台结论，以及上游 skip-list 或台账里的一句“无 API”，在写入台账、升级为 HARD-DIV 或引作本文依据之前自己补查一次；依据只引用本次实际读到的 d.ts 段落、skill 原文或参考条目，不把转述改写成“d.ts 无对应条款”。
5. 为平台差异设计替代开关或替换探测机制时，先列出源开关、源判据实际影响的路径与各返回分支的副作用；替代只作用于同一路径，只换判据、不合并分支，并在差异条目与验收中写明哪些路径不受影响。
6. 计划或台账写“执行已批准不可用 UX”一类汇总前，逐项核对所引决策是否覆盖该能力；不在内的单列为接入任务或待批决策。
7. 实现者只按差异条目列明的出口收敛；条目没覆盖的行为照源端实现，确需降级时登记为显式偏离或占位，不写成已实现。收到与源端基类行为冲突的开关接口位（如源端无条件开启前台派发，接口却要求按开关注册）时，回报规格冲突。差异决策的前提可以就地核对时（手边 SDK 声明里查得到所称不存在的接口，或理由只有成本、复杂度），回报决策冲突，不照写恒定状态、无效设置行或最小降级。

来源支持：25 张卡 · 已知 4 次迁移（部分未记录） · 已知 4 个应用（部分未记录）

## 来源（按需复核）

- [case-01833db0536ba02ed2ce](../../../store/cases/case-01833db0536ba02ed2ce/19be163e103f323f9d0fb55e1aa2516564a0df2af7f113771337fa3e7f3c8f79.json) · 结论：recommendation:1
  卡片版本：`19be163e103f323f9d0fb55e1aa2516564a0df2af7f113771337fa3e7f3c8f79`
- [case-29db923e9cadbe8ce53c](../../../store/cases/case-29db923e9cadbe8ce53c/aa92466b00c3c3bc5eadb4e83e006fcff79e7f08502b0bb49fa74f7777666761.json) · 结论：recommendation:3
  卡片版本：`aa92466b00c3c3bc5eadb4e83e006fcff79e7f08502b0bb49fa74f7777666761`
- [case-33b4b9ce51ba471ee770](../../../store/cases/case-33b4b9ce51ba471ee770/871dbcf0ed85e10b3dc05afa0ae591d090cd53dc24ad85bc90d89cbb0d6affe5.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`871dbcf0ed85e10b3dc05afa0ae591d090cd53dc24ad85bc90d89cbb0d6affe5`
- [case-3b8b620c1c7fa2848a34](../../../store/cases/case-3b8b620c1c7fa2848a34/2c8f9548575702e3dd4840957d2d99053daa0e3fe45f93f40765b5cabcb618bd.json) · 结论：recommendation:5
  卡片版本：`2c8f9548575702e3dd4840957d2d99053daa0e3fe45f93f40765b5cabcb618bd`
- [case-45230e39613edd881823](../../../store/cases/case-45230e39613edd881823/7949b6461d6df4d179e1766b8d90d9da28f6f5cd9816afaff2b4104f11ed15d7.json) · 结论：recommendation:2
  卡片版本：`7949b6461d6df4d179e1766b8d90d9da28f6f5cd9816afaff2b4104f11ed15d7`
- [case-6582e6c5e66cee6e4cc9](../../../store/cases/case-6582e6c5e66cee6e4cc9/9d68365c03023692c19a9bc475b1fd5ea85471ed54a31739edad54aa327b141d.json) · 结论：recommendation:1
  卡片版本：`9d68365c03023692c19a9bc475b1fd5ea85471ed54a31739edad54aa327b141d`
- [case-6984b2614fabe391f2e7](../../../store/cases/case-6984b2614fabe391f2e7/4e13e5e45b38251a019a68c084e9d1f1d2301fcf064ee28b4c8386bbcbbeb2b3.json) · 结论：recommendation:1
  卡片版本：`4e13e5e45b38251a019a68c084e9d1f1d2301fcf064ee28b4c8386bbcbbeb2b3`
- [case-730269321014e7e1d765](../../../store/cases/case-730269321014e7e1d765/d62d1ca408ead4c6087ee8493ffc6be944e20a88c5230ed7af8f16298d439621.json) · 结论：recommendation:1
  卡片版本：`d62d1ca408ead4c6087ee8493ffc6be944e20a88c5230ed7af8f16298d439621`
- [case-7456fcf259be55a8834b](../../../store/cases/case-7456fcf259be55a8834b/0fcbb858330dc0692a5ef76947e2ee1aae9990c5195f78148938c87b3ce94fe8.json) · 结论：recommendation:3
  卡片版本：`0fcbb858330dc0692a5ef76947e2ee1aae9990c5195f78148938c87b3ce94fe8`
- [case-76fcde297f6a5406e58f](../../../store/cases/case-76fcde297f6a5406e58f/4fe7565a766323ef4f1d2f178dcd030e8db4d702b78336c519b17cf80d48da0d.json) · 结论：recommendation:4, recommendation:5
  卡片版本：`4fe7565a766323ef4f1d2f178dcd030e8db4d702b78336c519b17cf80d48da0d`
- [case-7e6984a7fa6d5845737b](../../../store/cases/case-7e6984a7fa6d5845737b/28061d97667de8051e1a704ca4104b16d7db6a03989478ec6a0298430dae5dba.json) · 结论：diagnosis, recommendation:3
  卡片版本：`28061d97667de8051e1a704ca4104b16d7db6a03989478ec6a0298430dae5dba`
- [case-7f8dcb2d9341693d1225](../../../store/cases/case-7f8dcb2d9341693d1225/9bc002a9ae47b1515ae4f83a7641866747bdf2d6e5d4dae238785c21ea360875.json) · 结论：diagnosis, recommendation:1
  卡片版本：`9bc002a9ae47b1515ae4f83a7641866747bdf2d6e5d4dae238785c21ea360875`
- [case-8b307e33adf3d2817a04](../../../store/cases/case-8b307e33adf3d2817a04/2585469b6f2560d0a8b4e6ced070f91257eea43766cb634ab5779774aabdcc80.json) · 结论：recommendation:2, recommendation:5
  卡片版本：`2585469b6f2560d0a8b4e6ced070f91257eea43766cb634ab5779774aabdcc80`
- [case-8e426a5be8a17ead231c](../../../store/cases/case-8e426a5be8a17ead231c/4e2dc4057a637cdf01596cbbb248f5a8d6aa8a12596c92a5d3f1caacb17504b0.json) · 结论：recommendation:1, recommendation:4
  卡片版本：`4e2dc4057a637cdf01596cbbb248f5a8d6aa8a12596c92a5d3f1caacb17504b0`
- [case-a78ca40d4f9b42be76bb](../../../store/cases/case-a78ca40d4f9b42be76bb/7d12da37377f7c970931508bbb172dfde97532993727638bbbfba2a8f413f627.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:4
  卡片版本：`7d12da37377f7c970931508bbb172dfde97532993727638bbbfba2a8f413f627`
- [case-ac823e7436e1b08612ba](../../../store/cases/case-ac823e7436e1b08612ba/001e12d63eb0e435e0b1844db82cdbae78fc17a4ab6d1e93e6e523d3d5f4f174.json) · 结论：recommendation:1
  卡片版本：`001e12d63eb0e435e0b1844db82cdbae78fc17a4ab6d1e93e6e523d3d5f4f174`
- [case-be892688a05d8782271e](../../../store/cases/case-be892688a05d8782271e/0ae36d4e4a546c82b4b5f7f45cbb7e9843fceab665aabf81d810a3236c2985c6.json) · 结论：recommendation:3
  卡片版本：`0ae36d4e4a546c82b4b5f7f45cbb7e9843fceab665aabf81d810a3236c2985c6`
- [case-cbf23fa7a4ed42d37671](../../../store/cases/case-cbf23fa7a4ed42d37671/013c03becf2fdb81fe5d3bb32c60d6635f41ed3de130131a61605958b50d27f5.json) · 结论：diagnosis, recommendation:1
  卡片版本：`013c03becf2fdb81fe5d3bb32c60d6635f41ed3de130131a61605958b50d27f5`
- [case-d923c5dbfc1e66ce5f8b](../../../store/cases/case-d923c5dbfc1e66ce5f8b/543d2282bb0caf83001b49301e407e5e4256669899f59d4fbf9d64c789925c37.json) · 结论：diagnosis, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`543d2282bb0caf83001b49301e407e5e4256669899f59d4fbf9d64c789925c37`
- [case-d9c2b75062eb57796ca2](../../../store/cases/case-d9c2b75062eb57796ca2/c0e0684d2567560ee8d44f49d9c8eb3a4d4b3cc9ba5d7380a8e25a3b0f7792e8.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`c0e0684d2567560ee8d44f49d9c8eb3a4d4b3cc9ba5d7380a8e25a3b0f7792e8`
- [case-e5655934c3f8870c44d9](../../../store/cases/case-e5655934c3f8870c44d9/a4237b5912157b58b0850e3ddd1757e5ca48ae3bbbf0bd425ee7c766aee19544.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`a4237b5912157b58b0850e3ddd1757e5ca48ae3bbbf0bd425ee7c766aee19544`
- [case-ea77ad96a8fa0f09fbc8](../../../store/cases/case-ea77ad96a8fa0f09fbc8/6cd1f556630841a2ecd89461200b4ea6d26d01cbaca3eb1b97acaec296947081.json) · 结论：recommendation:2, recommendation:5
  卡片版本：`6cd1f556630841a2ecd89461200b4ea6d26d01cbaca3eb1b97acaec296947081`
- [case-ef167da8e80990c31714](../../../store/cases/case-ef167da8e80990c31714/b0741045842d4ef96db79c2bd8c9a99425324ad7612422a92bb274517b7f68a8.json) · 结论：recommendation:2
  卡片版本：`b0741045842d4ef96db79c2bd8c9a99425324ad7612422a92bb274517b7f68a8`
- [case-f3d590ba381f544833aa](../../../store/cases/case-f3d590ba381f544833aa/325219ee0b387ba129bb7f81d453f59f12c49ab4a600282dca41d129b45ee3f4.json) · 结论：recommendation:1
  卡片版本：`325219ee0b387ba129bb7f81d453f59f12c49ab4a600282dca41d129b45ee3f4`
- [case-f4fef12b5d994df457b2](../../../store/cases/case-f4fef12b5d994df457b2/1df73908a2600045d97b85fa5e386b5b50972e141d1cd5505d5df882f5ebbad2.json) · 结论：diagnosis, recommendation:1
  卡片版本：`1df73908a2600045d97b85fa5e386b5b50972e141d1cd5505d5df882f5ebbad2`

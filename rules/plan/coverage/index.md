# 覆盖清单与跳过清单

交回的是 skip-list、覆盖清单、对齐表、ui-manifest、feature-index，或债务闸、覆盖检查报出的 gap，以及被跳过、标「平台无对等」的条目时

## 触发族

- [交互对齐和覆盖审计](interaction-parity-audit/index.md)（6 条）：对齐表、覆盖清单、跳过清单、巡检单、路由 parity 校验里对源端点击、跳转、ViewModel 调用面的判定（✅、一致、已承接、已裁定、入口未渲染）
- [被改标签关掉的缺口和对齐项](gap-closed-by-relabel/index.md)（4 条）：债务闸、覆盖检查、编译门报出的 registry-gap、MANIFEST_ACTIVITY_UNACCOUNTED、decision-gap，或规格验收项，在回写清单、跳过清单、遗留披露、对齐表里被 retag、登记跳过、只记遗留或标「✅ 完全一致」，代码那一处却没实现
- [跳过清单和 unmapped 登记](skip-records/index.md)（4 条）：skip-list 或 resource-mapping 里写「平台无对等、降级」「跳过（unmapped）」「由某 feature 处理」，没有检索记录，也没有逐键登记被跳过的值和承接方
- [跳过清单里按引用计数归成平台胶水的文件](platform-glue/index.md)（1 条）：覆盖检查列出被引用却没锚定到任何 feature 的源文件（如广播接收器类），skip-list 按引用计数把它归为「平台胶水」，没核对回调里有没有业务调用
- [移除已登记的页面或弹窗](retired-pages/index.md)（1 条）：收口或返修回执写「已移除」「Removed …」某个页面或弹窗文件；ui-manifest 仍记为 verified，feature-index、ui-plan、placeholder-registry 和迁移报告没同步，也没引台账决策
- [按政策排除的功能簇在计划里的去向](excluded-feature-deferral/index.md)（1 条）：决策台账把某个功能簇（如桌面 Widget）按政策排除；计划把它的 parity AC 批量打上「superseded by」决策编号的墓碑、从 plan-coverage 的批次映射里删掉，没单列 deferred 批次

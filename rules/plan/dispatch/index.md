# 派工说明

交回的是给执行子代理的派工说明或派工补充：要交的源文件、前置 skill、必读清单、迁移陷阱编号、suggested_skills、控件映射和参数、另加的要求和限制、派发先后时

## 触发族

- [还原任务的派工](restore-dispatch/index.md)（2 条）：用户要求「对比安卓，还原某功能」时，派工里交给执行子代理的源工程路径、Screen / ViewModel 文件、页面行为要点和派发先后
- [派工里规格之外的余地和限制](dispatch-beyond-spec/index.md)（3 条）：派工给执行者另加规格映射行里没有的交互形态（如「或改用外链按钮」），或设「禁新造网络端点」这类和规格 AC 冲突的限制
- [页面转换派工的前置必读](converter-prereading/index.md)（3 条）：页面转换派工里的前置 skill 清单和要点名的错误模式：源端带状态参数的子控件要转成 @Builder 复用，或本会话刚出现过 ArkTS 组件语法报错（';' expected、Only UI component syntax）
- [资源 HARD-GATE 和页面转换器的派出时机](resource-hard-gate/index.md)（1 条）：执行规程要求 Stage 0 资源 HARD-GATE 先跑，Stage 0 还在运行时就派出了页面转换器，派工里没写资源仍在迁移
- [派工补充里改写的控件类型](dispatch-control-types/index.md)（1 条）：已审规格写了控件映射（如 CheckBoxPreference → Row + Checkbox），编排者的派工补充写成「CheckboxPreference→Toggle」「→箭头行」，和已审规格不一致
- [前台计时或动画引擎派工里的 tick 参数](tick-params/index.md)（1 条）：决策台账里有替代后台 Worker 的条目（如「500ms ticker + elapsedRealtime 补偿」），前台计时、动画引擎的派工照搬了这组参数，和该 feature 规格的映射行不符
- [限读派工的必读清单](must-read/index.md)（1 条）：页面有弹层、遮罩、叠层这类要定 hitTestBehavior 的交互，派工写了「效率纪律」一类限读要求，必读清单只有 pitfalls，没有交互映射参考的「触摸测试控制」表
- [派工里带的领域技能（suggested_skills）](skill-binding/index.md)（2 条）：可用技能清单或 skill 映射表里有对得上切片的领域技能（arkts-dark-mode、arkts-login、arkts-payment 等）；派工的 suggested_skills、派工技能里没带它，或把这个 SDK 判成三方 SDK 占位登记
- [派工里按编号点名的迁移陷阱](named-pitfalls/index.md)（1 条）：切片里有横向滚动的 Tab 行或标签条（PrimaryScrollableTabRow、horizontalScroll）、贴合内容的选中指示器（matchContentSize、fillMaxSize）；派工说明按编号列须遵守的迁移陷阱，却漏了对应的条目（P-22、P-20）
- [控件形制来自三方库时派工给的查值来源](third-party-lib-aar-lookup/index.md)（1 条）：规格或映射登记了三方库名和版本（如 material-dialogs → CustomDialog、preference-ktx 运行时构建），控件形制来自库资源、项目 res/ 里没有；派工只列了安卓源码路径，没写库 AAR 在 Gradle 缓存里的位置，也没提示解包查 values 和 layout
- [派工说明里要带的台账总则决策](dispatch-ledger-principles/index.md)（1 条）：决策台账里有「忠实复刻原版行为含缺陷；例外仅平台合规必需项」一类总则决策；派给 slice worker 或 closer 的说明里没有这条决策原文或「含缺陷复刻」要求，只让 grep 个别 PD- / D- 条目
- [用回调替换 @Monitor 的派工清单](monitor-to-callback-dispatch/index.md)（1 条）：原 @Monitor 只监听运行态、结果这几个字段，源端效果按目标值变化触发；派工或补丁方案把不改被监听字段的路径（如每代 tick 的提交尾部）列成回调触发点，没要求变化判断，还判为「语义等价」

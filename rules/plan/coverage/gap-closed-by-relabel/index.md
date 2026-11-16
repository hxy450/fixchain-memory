# 被改标签关掉的缺口和对齐项

agent 会看到什么：债务闸、覆盖检查、编译门报出的 registry-gap、MANIFEST_ACTIVITY_UNACCOUNTED、decision-gap，或规格验收项，在回写清单、跳过清单、遗留披露、对齐表里被 retag、登记跳过、只记遗留或标「✅ 完全一致」，代码那一处却没实现

## 规矩

- rule-0d68922c1fc6｜收尾闭环遇到 registry-gap 或 deferred-missing-artifact 时，打开占位处代码核对｜读到：债务闸报出占位的 registry-gap、deferred-missing-artifact 或 GAP；写错：回写清单把占位 retag 成「集成期」，或把 brief 里的依赖说法改写成「内联某组件或对应 service 承接」，没核对占位处代码仍是空桩
- rule-8276ae944de0｜被引用的 Activity 报未归属时补 page spec，不登记跳过清单｜读到：覆盖检查对截图页引用的 Activity 报 SPEC.MANIFEST_ACTIVITY_UNACCOUNTED，建议补 page spec 或锚入 feature；写错：skip-list 把这些 Activity 逐条登记为「首页可达说明页，路由契约保留」「个人中心可达目标，页面视觉后续增量」来关掉阻断
- rule-6066c649fdd0｜移交里记着「换成语义不同的替代」的 decision-gap 时，不只记遗留，回到生成期补查替代并修正｜读到：编译门的派工限定「不得改 spec 语义，已实现的行为代码只做编译级最小改动」；写错：编译门回报的 decision-gap 或迁移报告的遗留披露里写着：单调时钟已换成 Date.now() 墙钟（单调性不同），但没有对应的修正任务，代码保持墙钟
- rule-dcc9c33be954｜自报功能对齐前，按规格验收项逐条在当前文件检索实际组件和方法｜读到：规格验收项写有具体控件和交互（如勾选框切换完成状态）；写错：对齐表把这一项标「✅ 完全一致」，当前代码文件里却检索不到对应的组件（如 `Checkbox`）和 ViewModel 方法

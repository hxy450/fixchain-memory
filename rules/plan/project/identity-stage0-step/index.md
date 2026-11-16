# 资源迁移后的应用身份落地步骤

agent 会看到什么：资源迁移的派工或返回信封把应用身份（label、app_name、版本、图标）划给后续步骤并写「最终装配归属」；阶段规范要主线程在进 Stage 1 前调 arkts-app-identity（scope=dev-identity），编排记录、Stage 0 产物清单或完成报告里怎么交代这一步

## 规矩

- rule-082a690a3b46｜资源迁移按分工保留脚手架身份值时，返回信封逐项列出保留的键和接手步骤｜读到：派工把应用身份（label 文本、版本、图标）划给后续步骤，资源迁移只写 entry 的 resources；写错：返回信封只写「最终装配归属某步骤」，没有逐项列出保留为脚手架值的键（如 EntryAbility_label、AppScope 的 app_name）
- rule-278b0a52bb76｜推进到下一阶段前，核对阶段规范划给主线程的收尾步骤已实际调用，没调用就阻断｜读到：阶段规范写明某收尾步骤由主线程在子任务返回后单独执行（如资源迁移后、进入页面转换前自动调用应用身份落地，scope=dev-identity），子任务返回里也写着「最终装配归属」这一步；写错：编排记录在子任务返回后直接进入下一阶段，没有这一步的调用记录，报告里也没有登记为阻断项
- rule-8306a7d5965d｜Stage 0 的预期产物和完成报告要列身份映射，没执行就不进 Stage 1｜读到：执行流程的 Stage 0 说明要求资源迁移后、进 Stage 1 前由主线程调用 arkts-app-identity（scope=dev-identity）；写错：Stage 0 预期产物清单只列资源映射和占位登记，完成报告宣告 Stage 0 完成却没提身份映射，Stage 1 已经派发
- rule-6d9844094833｜stage 参考写明调用 App 身份 skill 时，派工按它的输出表逐项落地，不用自写要点｜读到：Stage 0 资源前置的 stage 参考写明资源迁移后、进 Stage 1 前调用 arkts-app-identity（scope=dev-identity）落地 app_name、versionName/versionCode、图标；写错：派工里身份落地被压成一条自写要点：只列 versionName/versionCode 和 module.json5 的 label，没有 startIcon.png、EntryAbility_label；待办里列了 app-identity 却没有调用记录
- rule-6b6ba9e4359c｜Stage 0 的 brief 只记了版本号和 label 时，补记身份 skill 的调用和输出文件再判完成｜读到：stage 参考要求 Stage 0 调用 arkts-app-identity（scope=dev-identity）；写错：Stage 0 的 brief 里身份一项只列 versionCode/versionName 和 module.json5 label，没有 skill 的调用记录和输出文件清单；续跑时凭 brief 存在就判定 app-identity 已经跑过

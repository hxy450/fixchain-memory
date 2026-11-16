# HAR 模块迁移批次的验收项

agent 会看到什么：页面、资源或代码在 HAR 模块之间迁移或写入 HAR，计划和批次验收只写「整包 assembleHap 通过」「真机跑通」，没有逐模块的 $r 名称、跨模块导入和 ArkTS 检查

## 规矩

- rule-4d4df39b0a15｜资源迁移的验收只写整包 assembleHap 或真机跑通时，补上逐模块的资源闭包检查｜读到：页面或资源在 HAR 模块之间迁移；写错：计划或验收只写「整包 assembleHap 通过」「真机一跳正常」，没有逐个 HAR 核对 $r 名称
- rule-6e4c121d5a35｜模块化或插桩批次的验收除 assembleHap 外，加两项搜索和按模块的 ArkTS 检查｜读到：派工是把代码迁入或写入 HAR 模块、调整跨模块导入的批次；写错：派工或批次验收里只有 assembleHap 构建通过一项，没有 HAR 目录里 from 'BuildProfile' 为 0、跨模块相对路径为 0 的搜索，也没有按模块的 ArkTS 检查

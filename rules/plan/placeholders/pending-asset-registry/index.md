# 未就绪资源资产的登记

agent 会看到什么：占位登记或交付说明里有资源未就绪的条目（resource-pending-asset、P-RES-ASSET、资产类 FWD-REF），触发条件写「资产就绪」、owner 或 resolve_by 留空、资源到位后仍是 registered，或源图分辨率远低于目标显示区却被放大充当正式资源

## 规矩

- rule-90a866b2fe26｜登记资源为 pending 前在写入时刻重列资源目录，沿用别人的 pending 先执行其触发条件｜读到：占位登记表里有资源未就绪的 pending 条目（如 `P-RES-ASSET-…`，触发条件「某字体就绪」）；写错：登记表把已经在 rawfile/fonts 下的字体登记成待定，或沿用这类条目时没执行它的触发条件
- rule-d709cd67e8f5｜确需延后接线的位图层，移交登记写明 owner 和可机械检查的断言，不只写「资产就绪」｜读到：派工规则把 resource-pending-asset 定义为「fallback 资产引用加 marker」，代码里留了 `FWD-REF` 资产类登记；写错：移交或占位登记行的 owner / resolve_by 留空，触发条件只写「资产就绪」「就绪后补 Image 层」，没有能机械检查的断言
- rule-df6d96f91423｜补资源后登记触发条件已满足时，先查代码槽引用了该资源，只有注释就指定 owner 接线｜读到：resource-pending-asset 类登记行的触发条件（资产进入目标 media）在补资源环节已满足；写错：补资源报告只写「仍需后续 wiring pass」没有指定 owner；登记行仍是 registered、resolve_by 的改动没有落盘；代码里同处仍只有 `FWD-REF` 注释
- rule-cc463ed22f91｜源图远小于目标显示区时，交付说明把它列为待设计方提供的大图，不以插值放大充当正式资源｜读到：源端只有远小于目标显示尺寸的位图（如 72px 对 450px 显示区）；写错：交付说明写「72px→1024px 放大，保留透明背景，符合规范」，没把源图分辨率不足列为待确认或待提供的资源

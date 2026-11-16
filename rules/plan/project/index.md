# 工程配置与模块

派工、移交、计划或报告涉及 module.json5（requestPermissions、方向、extensionAbilities、shortcuts）、app.json5（bundleName、vendor、label、icon、configuration）、form_config、应用身份步骤或 HAR 模块时

## 触发族

- [module.json5 配置项的移交](module-json5-handoff/index.md)（4 条）：派工、移交、返回信封或切片账本涉及 module.json5 的 requestPermissions（INTERNET）、extensionAbilities 注册、shortcuts 入口配置，而这个文件不在本任务的写权内，或写法没核实就写成确定指令
- [援引部署期决策跳过 bundleName / vendor](identity-skip-basis/index.md)（7 条）：skill、执行规范或派工写「scope=dev-identity，不碰 bundleName/vendor，属部署期决策（D-…）」，派工、跳过清单或报告沿用这个说法和编号作依据，而决策台账里没有这个编号、讲的是别的事，或台账技术项要求对齐源包名
- [资源迁移后的应用身份落地步骤](identity-stage0-step/index.md)（5 条）：资源迁移的派工或返回信封把应用身份（label、app_name、版本、图标）划给后续步骤并写「最终装配归属」；阶段规范要主线程在进 Stage 1 前调 arkts-app-identity（scope=dev-identity），编排记录、Stage 0 产物清单或完成报告里怎么交代这一步
- [HAR 模块迁移批次的验收项](har-acceptance/index.md)（2 条）：页面、资源或代码在 HAR 模块之间迁移或写入 HAR，计划和批次验收只写「整包 assembleHap 通过」「真机跑通」，没有逐模块的 $r 名称、跨模块导入和 ArkTS 检查
- [迁入 HAR 的页面的资源闭包](har-resource-closure/index.md)（1 条）：页面源码里有 $r('app.string/media/color.X') 或 getStringByNameSync 这类按名引用，迁移范围表或计划只列页面、VM、Service，没列 element 条目和 media 文件
- [module.json5 移交项里的方向配置](orientation-handoff/index.md)（4 条）：决策台账有横竖屏方向的决策、页面有 mediaquery 的 orientation 分支或 onConfigurationUpdate，派给收尾者的 module.json5 移交项只有 requestPermissions，报告说「无新增需求」
- [规格和插件要的权限与 module.json5 的 requestPermissions](permissions/index.md)（7 条）：规格有 uses-permission 映射段、应用经 permission_handler 请求 Permission.xxx、插件 OHOS 实现里有 requestPermissions / ohosPermissions，计划没有任务落到 module.json5，或插件记录凭构建通过标 verified / build_verified
- [派工里的服务卡片规格（form_config）](widget-form-config/index.md)（1 条）：源 res/xml 的 appwidget-provider 写了 targetCellWidth / targetCellHeight、minResizeWidth、maxResizeWidth、resizeMode；台账或派工里的 supportDimensions、defaultDimension 是默认假设，没写出自源的哪一项，没有 resizable，已批的静态预览没带进派工
- [应用身份和外壳派工的核对范围（app.json5 configuration）](identity-dispatch-configuration/index.md)（1 条）：读到决策台账判大字体为迁移，或源端有随系统字号缩放的文本；应用身份 / 应用外壳的派工范围只列 app_name、versionName、versionCode、icon，没有 app.json5 的 configuration，完成自检里也没有核对 profile
- [分享接收入口的 Ability 和 skills 声明](share-receive-ability/index.md)（1 条）：参考规格写分享接收是 SEND + DEFAULT + mimeType text/plain、launchMode 未声明即 standard；台账或派工把 actions=[ohos.want.action.sendData]、entities=[entity.system.home]、type=text/plain 挂在入口 Ability 上，或写「EntryAbility onCreate/onNewWant 分支有确定写者」

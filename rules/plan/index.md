# 计划与派工（plan）

133 个族，353 条规矩。整个产物的族一页看完见 [map.md](map.md)（每个主题一行，下面是「短号 族名（条数）」）。

## 一级主题

- [构建与编译](build/index.md)（8 条）：派工里写了禁止 worker 编译、不跑 hvigor、附 ArkTS 限制清单，或者交回的报告、回执、CHECK-1、编译门报告里写了构建结果（BUILD SUCCESSFUL / FAILED、0 errors、编译尚未执行）时
- [覆盖清单与跳过清单](coverage/index.md)（17 条）：交回的是 skip-list、覆盖清单、对齐表、ui-manifest、feature-index，或债务闸、覆盖检查报出的 gap，以及被跳过、标「平台无对等」的条目时
- [数据、网络与日志](data/index.md)（5 条）：源端有 Retrofit Service、BuildConfig.BASE_URL、鉴权拦截器、Room Migration、偏好标记，或者台账列了日志边界，计划和契约要写网络层、数据库、偏好接口、日志任务时
- [决策台账与决策缺口](decisions/index.md)（10 条）：读到的决策台账、PD 决策卡、规格里的条件或作用域限定和源码、派工对不上，交回的 decision_gaps、handback、巡检问题单里要记分歧或延后裁决时
- [派工说明](dispatch/index.md)（18 条）：交回的是给执行子代理的派工说明或派工补充：要交的源文件、前置 skill、必读清单、迁移陷阱编号、suggested_skills、控件映射和参数、另加的要求和限制、派发先后时
- [修复工单与问题单](fix/index.md)（6 条）：交回的是修复工单、问题文件、UT 分诊、修复报告或修复回执：工单建议的修法、RED 用例、§6 预期效果、按截图删减、本轮不修的偏差时
- [交回报告与完成说法](handback/index.md)（34 条）：交回的回执、交付说明、收口报告、转换报告、slice notes 里写着「已实现」「已补齐」「已对齐」「全部完成」「resolved」「均保留」这类完成说法时
- [交接摘要与移交项](handoff/index.md)（12 条）：交回的交接摘要、契约摘要、计划或 TODO 里转述源端方法的行为，或者上游交接、子代理回执写明某项交给别的任务、主线程或后续切片承接时
- [入口与生命周期](lifecycle/index.md)（18 条）：源端 Application、Activity 和业务基类的 onCreate、onResume、onPause、onDestroy、onBackPressed 里有行为，或者目标端要接到 EntryAbility、入口页、共享服务的停止和释放上时
- [占位登记与前向引用](placeholders/index.md)（79 条）：交回的产物里有 placeholder-registry 条目、FWD-REF / UNC 标记、// HANDOFF: 行、resolve_by、近似项或资源未就绪的登记，或者有留给后续切片的交互、数据和事件时
- [切片计划与重构计划](plan/index.md)（14 条）：交回的是切片计划、重构计划、批次与模块拆分或改动清单：scope、acceptance、integration_points、Step、跨业务依赖，以及换了承接方的源端职责时
- [工程配置与模块](project/index.md)（33 条）：派工、移交、计划或报告涉及 module.json5（requestPermissions、方向、extensionAbilities、shortcuts）、app.json5（bundleName、vendor、label、icon、configuration）、form_config、应用身份步骤或 HAR 模块时
- [资源](resources/index.md)（15 条）：派工、交接、资源映射报告或收口回报涉及 strings.xml / string.json、colors.xml / color.json、$r 令牌、多语言、图标和 SVG 资源的来源与转换结果时
- [三方 SDK 与插件](third-party/index.md)（3 条）：规格、skill 映射表、pubspec 或 .flutter-plugins-dependencies 里有要平台 Key 的厂商 SDK（如 com.amap.api）、Flutter 插件和它依赖的原生插件时
- [界面](ui/index.md)（70 条）：读到的源码或规格里有窗口与系统栏、弹窗、布局尺寸、列表、共享组件、页面路由、主题、吐司和通知这类界面写法，派工、登记、计划或报告要交代它们时
- [验证报告与验收结论](verification/index.md)（11 条）：交回的验证汇总、视觉校验、阶段报告、差异清单、巡检单、收尾一致性结论里有 PASS、✔、BLOCKED 判定，或者有要真机、截图才能确认的项时

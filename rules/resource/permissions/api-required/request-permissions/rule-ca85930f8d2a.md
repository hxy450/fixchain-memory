# module.json5 同时声明模糊和精确定位权限，构建权限警告逐项对照

审的是：资源
触发（任一种）：
- 读到：源端 AndroidManifest 同时声明 ACCESS_FINE_LOCATION 和 ACCESS_COARSE_LOCATION；代码里调用 geoLocationManager.getCurrentLocation；写错的样子：module.json5 的 requestPermissions 只有 ohos.permission.LOCATION 一项（照抄代码里的单个字符串）
- 读到：构建日志有 WARN「To use this API, you need to apply for the permissions: ohos.permission.APPROXIMATELY_LOCATION」；写错的样子：requestPermissions 里没有警告点名的权限，构建仍按错误数判 PASS
适用范围：目标工程 module.json5 声明定位等 user_grant 权限、以及收口构建核对权限时
做法：
- requestPermissions 写两项：{ name: 'ohos.permission.APPROXIMATELY_LOCATION', reason: '$string:…', usedScene: { abilities: [...], when: 'inuse' } } 和同样结构的 ohos.permission.LOCATION
- 构建日志出现「To use this API, you need to apply for the permissions: X」时，与 requestPermissions 逐项对照，缺项补上，不判 PASS
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- APPROXIMATELY_LOCATION 与 LOCATION 是 user_grant 权限，reason 和 usedScene 必填：两项都要带 reason、usedScene（出处：declare-permissions.md，声明样例）
- usedScene.when 只能填 inuse 或 always：使用时机的取值（出处：declare-permissions.md，在配置文件中声明权限）
- module.json5 增加 APPROXIMATELY_LOCATION 并联合申请后，权限警告消失、先授权后定位通过回归测试：补齐声明后定位链路正常（出处：卡里修好并验证过）
未核实：构建警告原文出自卡里的构建日志，本机声明和文档副本里没有找到这句
来源：1 张卡，1 个应用
- case-8c249997059a2524ea7b（app_hnaccurateweather_live_android）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 5；取值 3 ← 诊断

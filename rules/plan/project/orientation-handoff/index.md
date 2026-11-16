# module.json5 移交项里的方向配置

agent 会看到什么：决策台账有横竖屏方向的决策、页面有 mediaquery 的 orientation 分支或 onConfigurationUpdate，派给收尾者的 module.json5 移交项只有 requestPermissions，报告说「无新增需求」

## 规矩

- rule-0c2a3e214954｜module.json5 的移交项要带方向配置；页面有横屏分支而没有 orientation 时登记为缺口｜读到：决策台账有横竖屏方向的决策；页面实现里有 `mediaquery` 的 orientation 分支或 `onConfigurationUpdate` 重选横屏布局；写错：派给收尾者的 module.json5 移交项只有 requestPermissions；收尾或实现者的报告说 module.json5「无新增需求」，没有把缺 orientation 登记为缺口
- rule-1e33c9f2c035｜计划逐项核对 Manifest 解析和平台目标值表，每个配置项落进某个 slice，没取用的列为待指派｜读到：页面规格「Manifest 解析」行、参考规格平台目标值表里同一行列了几项落在配置文件或窗口级 API 的目标值（如 module.json5 的 orientation 与窗口的 RESIZE 同行）；写错：计划只取用了其中一部分（如只把 RESIZE 写进某个 Step），其余项（如 module.json5 EntryAbility 的 orientation）没有出现在任何 slice 或 Base step 的 scope 里，也没列为待指派
- rule-83c47d48eaa2｜规格要改本页输出以外的配置文件时，登记 deferred-work 并在返回信封列出｜读到：规格要求修改本页输出文件以外的配置文件（如「module.json5 EntryAbility orientation: …」），登记表约定 module.json5 配置属 deferred-work、归属步骤或触发条件必填；写错：只在转换报告的「交由后续」里写一句（如「module.json5 orientation=… → 入口装配段」），占位登记表里没有 kind=deferred-work 的条目，返回信封也没列；或交给职责不覆盖该项的步骤（如入口 Navigation 装配）
- rule-85b03972c490｜orientation、launchType 要指定步骤认领，派工不能整体写 module.json5 不改｜读到：AndroidManifest.xml 的 <activity> 带 android:configChanges 含 orientation、android:launchMode，未写 android:screenOrientation；写错：派工写「app.json5 / module.json5 不改」，或把 module.json5 的改动限定在身份字段（名称、版本、图标），而 EntryAbility 的 orientation、launchType 没有任何步骤认领

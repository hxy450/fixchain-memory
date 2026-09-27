# 决策已批准等价实现的平台能力要真实现，只在运行期按实际结果降级；判定“平台没有”前先查本地 SDK 声明，确需替代就显式登记

ID：`lesson-efb94f2d70d4df1c65d7` · 版本：1

[本主题](index.md)

## 何时使用

实现平台服务（后台任务、进度通知、通知授权、画中画回退、动态取色等）或解决指向平台切片的前向占位时

## 适用情境

源端依赖系统后台 Worker、带动作的进度通知、通知权限、画中画或 Material You 动态取色；决策账本已为这些能力批准“等价平台抽象”或“应用内回退”方案，而不是延期。

## 例外与边界

- 决策账本对该能力明确批准的是延期或仅前台实现

## 原因

把“禁止伪造进度”读成可以不实现，会写出恒 false、两支相同的桩，报告仍标已接线；把“一时没找到 API”当成结论，会私自降级。来源中接手的编排者把后台计时服务写成恒定“仅前台”、持久化恒 false、授权强制 false，违背已批准的等价实现决策；修复轮一个 worker 认定没有壁纸取色接口，把动态主题降成颜色模式切换，下一轮在本地 SDK 查到 @ohos.wallpaper 的 getColors 与 on('colorChange')；另一个 worker 用通用通知槽替代具名高重要度渠道，没有声明这项替代。

## 做法

1. 实现前读决策账本该条目选定的方案；“禁止伪造”只约束失败时如实上报，不等于可以不实现。
2. 服务层写出能力检测、权限请求（如 notificationManager.requestEnableNotification）、长时任务（backgroundTaskManager.startBackgroundRunning，并在 module.json5 声明 ohos.permission.KEEP_BACKGROUND_RUNNING 与对应 backgroundModes）、通知动作（WantAgent），失败时返回可观察的原因。
3. 判定平台无对等能力前，在本地 SDK 的 ets/api/*.d.ts 里查（含标记 deprecated 的接口）；确需替代时把“源端能力 → 目标实现”写成显式映射，并登记到迁移报告或决策账本，不在实现里默默降级。
4. 自检：对本次实现的函数 grep 恒定返回和“? X : X”，再与账本里 approved 的实现类决策逐条对照。

## 来源（按需复核）

经验是有适用范围的历史建议。核查来源时同时看结论与 unknown；来源卡未随阅读包复制。

- case-470d704a6ec794b4c3c9 · 结论：recommendation:3
  卡片版本：`13ef866ddad634597d116308c049409fa19b886ac8827aba7a1101eafd7c59af`
- case-e92bb15630afd5b03216 · 结论：recommendation:1
  卡片版本：`35af48b5ba035c5b0a013f22aa96e74f8f156be000fe8cf630a6955219f940ce`
- case-f93a2f80bafd58105489 · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:4
  卡片版本：`12e7ff65fe7f72812a91eb79651ac8b7b03b6eb2bea044ceef693bb141cfa9d5`

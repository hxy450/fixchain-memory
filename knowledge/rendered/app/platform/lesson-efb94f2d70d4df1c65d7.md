# 决策已批准等价实现的平台能力要真实现，只在运行期按实际结果降级；判定“平台没有”前先查本地 SDK 声明，确需替代就显式登记

## 何时使用

实现平台服务（后台任务、进度通知、通知授权、画中画回退、动态取色、地图承载等）或解决指向平台切片的前向占位时

## 适用情境

源端依赖系统后台 Worker、带动作的进度通知、通知权限、画中画、Material You 动态取色，或用第三方地图 SDK 的 MapView 显示当前位置与轨迹；决策账本已为这些能力批准“等价平台抽象”“可验证的平台承载”或“应用内回退”方案，而不是延期。也包括规格把地图、POI 与导航列为核心功能并要求经能力适配层隔离，台账只批准了认证、广告、微信等少数能力的不可用降级，厂商 SDK 的 Key 尚未提供，计划汇总行却写“地图执行已批准不可用 UX”。

## 例外与边界

- 决策账本对该能力明确批准的是延期或仅前台实现
- 第 2 步的长时任务只在后台业务属于平台列出的类型（数据传输、音视频播放、录制、定位导航、蓝牙、音视频通话等）并且确实在执行时成立；源端后台工作不属于这些类型（如单纯的后台计时）时，startBackgroundRunning 不是等价实现，申请了也会因业务不符被挂起或终止。这时前台照源端真实现、挂起后交代理提醒等系统通道接续，不算桩，也不要硬套长时任务

## 原因

把“禁止伪造进度”读成可以不实现，会写出恒 false、两支相同的桩，报告仍标已接线；把“一时没找到 API”当成结论，会私自降级。来源中接手的编排者把后台计时服务写成恒定“仅前台”、持久化恒 false、授权强制 false，违背已批准的等价实现决策；修复轮一个 worker 认定没有壁纸取色接口，把动态主题降成颜色模式切换，下一轮在本地 SDK 查到 @ohos.wallpaper 的 getColors 与 on('colorChange')；另一个 worker 用通用通知槽替代具名高重要度渠道，没有声明这项替代。另一应用里决策要求地图用“平台能力的可验证承载”，实现者读过源端地图视图、定位 marker 与缩放逻辑，仍把定位成功态写成白底加定位标记图片，并把巡检项标为已解决；规格未点名地图组件、计划没有地图接入任务，占位一直保留到用户发现页面空白。

## 做法

1. 实现前读决策账本该条目选定的方案；“禁止伪造”只约束失败时如实上报，不等于可以不实现。
2. 服务层写出能力检测、权限请求（如 notificationManager.requestEnableNotification）、长时任务（backgroundTaskManager.startBackgroundRunning，并在 module.json5 声明 ohos.permission.KEEP_BACKGROUND_RUNNING 与对应 backgroundModes）、通知动作（WantAgent），失败时返回可观察的原因。
3. 源端地图视图落成真实地图组件（平台 Map Kit 或已决策的三方地图 SDK）并绑定定位坐标；key、client_id 等配置缺失而无法接入时显示“地图服务未配置”一类真实状态并登记缺口，不以静态图片冒充地图态或把巡检项标为已解决。规格或计划阶段把这类替代写成具体任务：目标组件与依赖、配置注入方式、坐标系换算和未配置态验收。
4. 判定平台无对等能力前，在本地 SDK 的 ets/api/*.d.ts 里查（含标记 deprecated 的接口）；确需替代时把“源端能力 → 目标实现”写成显式映射，并登记到迁移报告或决策账本，不在实现里默默降级。
5. 自检：对本次实现的函数 grep 恒定返回和“? X : X”，再与账本里 approved 的实现类决策逐条对照。
6. Key 等配置缺失只让运行期返回不可用：注册真实适配器并在缺 Key 时回退，不把不可用适配器作为默认且唯一的实现；规格与汇总行矛盾时把缺口写入决策缺口或登记三方 SDK 占位，回执写明“未接入”，不报告该功能完成。

来源支持：6 张卡 · 3 次迁移 · 3 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 2 步〕notificationManager.requestEnableNotification 拉起通知授权弹窗让用户选择是否允许发通知，要在应用界面加载完成后调用；用户拒绝后不能再用它拉起弹窗，要改用 openNotificationSettingsWithResult 二次申请
- 〔做法第 2 步〕backgroundTaskManager.startBackgroundRunning 需要 ohos.permission.KEEP_BACKGROUND_RUNNING；申请成功后通知栏显示与长时任务关联的消息，用户点它时拉起传入的 wantAgent 指向的 ability，用户删除这条消息时系统自动停止长时任务
- 〔原因 / 做法第 2 步〕安卓 NotificationManager.IMPORTANCE_HIGH（值 4）：到处显示、发声并浮动提示（peek），可用全屏 intent
- 〔原因 / 做法第 2 步〕notificationManager.SlotType.SERVICE_INFORMATION 对应 SlotLevel.LEVEL_HIGH：通知开启，状态栏显示图标，有提示音和横幅
- 〔原因 / 做法第 2 步〕NotificationRequest.notificationSlotType 不写时为 OTHER_TYPES，通知不会落到具名的高重要度槽
- 〔做法第 3 步〕Map Kit 的 map.convertCoordinate 目前只支持从 WGS84 转到 GCJ02
- 〔适用情境 / 原因〕@ohos.wallpaper 从 API 9 起把壁纸管理接口调整为系统 API，壁纸切换只能由系统应用完成；getColors、on('colorChange') 自 API 7 提供、自 API 9 废弃，公开接口里没有替代

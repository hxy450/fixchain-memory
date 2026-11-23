# 平台差异只收敛确实做不到的那一步：写“无对等”前查证并记录，替代方案只作用于源端同一路径，其余出口、分支与回退照源端保留

## 何时使用

规格提取与计划决策阶段，为源端平台专有能力（系统派发入口、商店跳转、系统设置深链、跨应用拉起、设备能力探测、运行时开关、画中画等系统窗口能力、系统取色、后台执行与通知动作），或目标没有现成组件的视觉与交互效果，登记平台差异、skip 或“已批准不可用”时；实现阶段消费这类差异决策时

## 适用情境

源端某条链路里只有个别步骤在目标平台确实做不到（如第三方不能运行时启停 skill、查询他包安装与运行状态），规格或台账却把整条入口判为“无对等”、把按钮出口改成说明文案、把不同探测结果合并成一个分支，或把替代开关接到源开关不影响的路径；计划汇总行把只批给少数能力的降级泛化到其他能力；实现者再把差异决策扩展到决策未列明的行为（如整段富文本链接都不实现）。“已查证”的说法可能没有对应的查询记录，或依据只是本地参考文件检索无命中、凭记忆断言。也包括目标只是没有现成组件或同名 API、可用滚动回调或 Canvas/Path 等通用能力组合实现的效果，被写成“简化为固定形态”；源码自带版本门槛与“不支持时回退”分支的能力被整体删除；源端检测手段在目标没有同名对应，被判定的状态却可以观察；子代理回执标为“存疑”的推断，或上游 skip-list 里的一句“无 API”，被下游升级为定论或改写成“d.ts 无对应条款”的依据。

## 例外与边界

- 决策记录明确批准了更大范围的收敛，并写明理由与用户可见影响
- 命中的接口是系统接口（声明标 @systemapi，文档写“此接口为系统接口”）而目标是普通应用（签名配置里应用类型为 hos_normal_app，新建工程默认如此）时，普通应用调用会以 202 失败，DevEco 自带的 public SDK 也不含这些接口：这一步按做不到登记并保留源端的失败回退，不作为“该接口 + 回退”交审批；已弃用或需权限的接口仍按第 2 步交审批

## 原因

“不能动态禁用”推不出“整条入口无对等”，“不能查询他包状态”推不出“不需要商店跳转”，“检测手段没有同名 API”推不出“行为删除”，“没有现成组件或同名 API”也推不出“只能简化”；差异范围一旦写大，下游会照单删掉源端仍可实现的出口、分支和回退，或把开关接到错误路径（关掉开关后前台功能也失效）。未执行的查证、子代理标为存疑的推断和汇总行里的泛化，经过转述都会被后续阶段当作已批准事实。来源中一个应用三处如此：清单声明的贴卡拉起入口被判为无对等、自启动开关改成了前台派发闸门；商店、设置深链与拉起他应用的出口被收敛为说明文本，“有 NFC 无 MFC”与“无 NFC”合并成同一分支；只涉及外跳出口的差异被扩大成正文链接都不实现。另一应用的计划汇总行把仅限认证、广告、微信的降级写成“地图执行已批准不可用”。

## 做法

1. 平台差异只收敛做不到的那一步（如他包状态恒为未知），源端按钮出口与回退链原样保留为“尝试 + 失败回退”（如 market:// 失败转 https 网页、设置子页失败退设置首页、拉起失败静默）；源码自带版本门槛或“不支持时回退”分支的能力，映射为“能力探测 + 原回退”，相关设置项的可用状态绑定探测结果。
2. 写“无对等/HARD-DIV/已查证”前，实际查项目 SDK 的 d.ts（ets/api、hms/ets/api 与 kits 导出，按能力关键词检索）、平台 skills 与能力文档，以及工程内现有的 startAbility、viewData 用法；把检索词、命中模块及其 @since、@deprecated、@systemapi、@permission 标注写进映射行。只检索了本地参考文档、映射表或凭记忆得出的“没有条目”，记为未查证，不升级为裁剪、HARD-DIV 或替代形态（例：固定桌面快捷方式、geo: 隐式拉起、整应用重启，在公开 SDK 中分别有 productViewManager.requestNewPinShortcut（HarmonyOS 专有接口，5.0.2(14) 起）、bundleManager.canOpenLink（API 12 起，链接的 scheme 要列在 querySchemes 里）、ApplicationContext.restartApp（API 12 起））。查不到就登记待定、交决策关口，不引用未执行的查证。只命中已弃用、仅系统可用或需权限的接口时，在决策中写出风险、失败回退与真机验证项，供审批在“降级”与“该接口 + 回退”之间选择，不写成无对等。决策关口收口时核对依据真实存在，并与同类裁决保持一致。
3. 目标只是没有现成组件或同名 API 时，先核对能否用通用能力组合实现（滚动回调加高度动画、Canvas/Path 自绘与动画、锚点加纯计算）；能实现就写成实现项并附源端参数，不登记平台差异。源端判定手段没有同名对应时，先写出用户可观察的条件与效果，再找目标上能观察到同一状态的信号。
4. 子代理回执标为“存疑/待定夺”的平台结论，以及上游 skip-list 或台账里的一句“无 API”，在写入台账、升级为 HARD-DIV 或引作本文依据之前自己补查一次；依据只引用本次实际读到的 d.ts 段落、skill 原文或参考条目，不把转述改写成“d.ts 无对应条款”。
5. 为平台差异设计替代开关或替换探测机制时，先列出源开关、源判据实际影响的路径与各返回分支的副作用；替代只作用于同一路径，只换判据、不合并分支，并在差异条目与验收中写明哪些路径不受影响。
6. 计划或台账写“执行已批准不可用 UX”一类汇总前，逐项核对所引决策是否覆盖该能力；不在内的单列为接入任务或待批决策。
7. 实现者只按差异条目列明的出口收敛；条目没覆盖的行为照源端实现，确需降级时登记为显式偏离或占位，不写成已实现。收到与源端基类行为冲突的开关接口位（如源端无条件开启前台派发，接口却要求按开关注册）时，回报规格冲突。差异决策的前提可以就地核对时（手边 SDK 声明里查得到所称不存在的接口，或理由只有成本、复杂度），回报决策冲突，不照写恒定状态、无效设置行或最小降级。

来源支持：26 张卡 · 已知 5 次迁移（部分未记录） · 已知 5 个应用（部分未记录）

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的平台资源；android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕Settings.ACTION_NFC_SETTINGS 的说明写明：有些情况下可能没有匹配的 Activity，调用方要自行防范
- 〔做法第 1、2 步〕bundleManager.canOpenLink(link) 返回链接能否打开；链接的 scheme 不在 querySchemes 里时抛 17700056
- 〔何时使用 / 做法第 1 步〕PiPWindow.isPiPEnabled() 返回当前系统是否启用了画中画
- 〔适用情境 / 做法第 5 步〕NfcAdapter.getDefaultAdapter(context) 在设备没有 NFC 适配器时返回 null
- 〔做法第 2 步〕ApplicationContext.restartApp(want) 重启应用并拉起指定的 UIAbility，重启时不触发 onDestroy；应用不在界面顶层时抛 16000053，目标不属于本应用或不是 UIAbility 时抛 16000063，两次重启间隔不足 3 秒时抛 16000064
- 〔做法第 2 步〕productViewManager.requestNewPinShortcut(context, tid) 在用户拒绝添加快捷方式时以 1006620007 失败；它是 HarmonyOS 专有接口，声明在 hms 下，标 @since 5.0.2(14)
- 〔何时使用 / 做法第 2 步〕wallpaper.getColors（Promise 和 AsyncCallback 两种重载）与 wallpaper.on('colorChange') 在公开 SDK 声明里仍然存在，都标 @deprecated since 9
- 〔做法第 2 步〕真机上调用已标弃用的 wallpaper.getColors 能取到壁纸主色，以它为种子生成的动态配色在界面上生效
- 〔做法第 2 步〕reminderAgentManager.publishReminder 的声明标 @permission ohos.permission.PUBLISH_AGENT_REMINDER，调用需要这个权限
- 〔做法第 3 步〕List 的 onScrollFrameBegin 在每帧滚动开始前回调，offset 是这一帧将要滚动的量（单位 vp），回调返回的 offsetRemain 是实际让列表滚动的量
- 〔做法第 3 步〕平台插值器 @android:interpolator/fast_out_slow_in 是 pathInterpolator，控制点为 (0.4, 0)、(0.2, 1)；objectAnimator 的 valueType=pathType 表示取值是路径字符串，用于 AnimatedVectorDrawable 的路径形变
- 〔做法第 3 步〕ArkUI 的 Curve.FastOutSlowIn 是 cubic-bezier(0.4, 0.0, 0.2, 1.0)
- 〔做法第 3 步〕三键导航时，TYPE_NAVIGATION_INDICATOR 避让区的 bottomRect.height 为 0，三键导航栏的高度落在 TYPE_SYSTEM 避让区的底部
- 〔做法第 3 步〕ApplicationInfo.appProvisionType 是应用签名证书文件的类型，取 'debug' 或 'release'；从 bundleManager 取自身 BundleInfo 时要带 GET_BUNDLE_INFO_WITH_APPLICATION，返回的 bundleInfo 才含 applicationInfo
- 〔做法第 5 步〕PackageManager.setComponentEnabledSetting 设置的是包内单个组件（activity、receiver、service、provider）的启用状态，覆盖该组件在清单里声明的启用状态
- 〔适用情境 / 做法第 5 步〕鸿蒙读 NFC 标签分前台读写和后台读写两条路径：前台读写由应用在前台的刷卡页面用 tag.registerForegroundDispatch 或 tag.on 动态注册，不需要在 module.json5 静态声明，切到后台时要取消注册；后台读写在 module.json5 静态声明标签技术类型，设备触碰标签后分发给能处理的应用，匹配到多个时弹出应用选择器
- 〔适用情境 / 做法第 5 步〕后台读取 NFC 标签的 skills 声明里，actions 必须包含 "ohos.nfc.tag.action.TAG_FOUND"；uris 的 type 前缀必须是 "tag-tech/"，后接 NfcA、NfcB、NfcF、NfcV、IsoDep、Ndef、MifareClassic、MifareUL、NdefFormatable 之一，填写错误会造成解析失败
- 〔做法第 1 步〕MediaRecorder.setMaxFileSize 的单位是字节，到达上限时以 MEDIA_RECORDER_INFO_MAX_FILESIZE_REACHED 通知并由录制器停止录制（停止是异步的）；传 0 或负数表示不限
- 〔做法第 1 步〕AVRecorderConfig 里有 maxDuration，没有文件大小上限的字段
- 〔何时使用〕NotificationRequest.template 的 NotificationTemplate.name 目前只支持 downloadTemplate
- 〔何时使用〕skills 的 uris 里 maxFileSupported 表示对指定类型的文件一次能接收或打开的最大数量，要和 utd 配合使用，缺省值为 0

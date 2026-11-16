# 调 getOAID 前在隐私协议同意之后检查并申请 APP_TRACKING_CONSENT，全零串按未授权处理

审的是：代码
触发（任一种）：
- 读到：目标要调用 identifier.getOAID()；规格接口表写 OAID 拒绝授权时返回全 0；写错的样子：直接调 getOAID()，前面没有 checkAccessToken / requestPermissionsFromUser，或不在隐私协议同意之后；把 00000000-0000-0000-0000-000000000000 当成有效 OAID 上送，或去掉了超时兜底
适用范围：目标端采集 OAID 的那段服务代码
做法：
- 隐私协议同意门之后用 abilityAccessCtrl.createAtManager() 的 checkAccessToken(tokenID, 'ohos.permission.APP_TRACKING_CONSENT')，未授权时 requestPermissionsFromUser(context, ['ohos.permission.APP_TRACKING_CONSENT'])，再调 getOAID()
- 返回全零串视为未授权（打告警、不当有效值），保留超时兜底
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- checkAccessToken(tokenID: number, permissionName: Permissions): Promise<GrantStatus>：AtManager 查是否已授权（出处：鸿蒙 SDK 的 ets/api/@ohos.abilityAccessCtrl.d.ts，AtManager.checkAccessToken）
- requestPermissionsFromUser(context: Context, permissionList: Array<Permissions>): Promise<PermissionRequestResult>：AtManager 弹窗向用户申请（出处：鸿蒙 SDK 的 ets/api/@ohos.abilityAccessCtrl.d.ts，AtManager.requestPermissionsFromUser）
- 未授权时 getOAID 得到 00000000-0000-0000-0000-000000000000：全零串表示没拿到授权（出处：鸿蒙 SDK 的 ets/api/@ohos.identifier.oaid.d.ts，identifier.getOAID）
- 协议门后的检查与申请、全零告警补齐后采集链接通：修好后的做法（出处：卡里修好并验证过）
针对本应用要查的：
- 隐私协议同意门在哪：目标工程里处理首启隐私协议的页面或服务，找同意后的回调；权限检查和申请放在这个回调之后执行
来源：1 张卡，1 个应用
- case-5c6be3ec08184086fd79（DeepAI全能PPT）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2；取值 4 ← 诊断

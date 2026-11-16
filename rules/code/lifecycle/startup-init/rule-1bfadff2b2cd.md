# 微信回调由 EntryAbility 的 onCreate、onNewWant 把 want 交给 handleWant

审的是：代码
触发（任一种）：
- 读到：源端 WXEntryActivity / WXPayEntryActivity 里 handleIntent(getIntent(), this) 接微信回调；写错的样子：EntryAbility 的 onCreate / onNewWant 没把 want 交给 WXApi.handleWant，回调页只留 FWD-REF 空实现，onResp 没人调用
适用范围：接入鸿蒙版微信 OpenSDK，迁移源端的微信回调 Activity 时
做法：
- EntryAbility 的 onCreate(want, launchParam) 和 onNewWant(want, launchParam) 里先把 want 交给 WXApi.handleWant(want, 处理器)，再走其他路由
- 处理器的 onResp 按回调类型分派登录和支付结果
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): void：冷启动拉起时的入口（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.UIAbility.d.ts，UIAbility.onCreate）
- onNewWant(want: Want, launchParam: AbilityConstant.LaunchParam): void：已在后台的实例被再次拉起（热启动）时的入口，微信返回时多走这里（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.UIAbility.d.ts，UIAbility.onNewWant）
- EntryAbility 先把 Want 交给微信回调再路由，onResp 按类型分派后链路可用：修好的做法（出处：卡里修好并验证过）
未核实：WXApi.handleWant 的签名在三方包里，本机知识库没有声明可核
来源：1 张卡，1 个应用
- case-febf3c781ebde9778c30（DeepAI全能PPT）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 诊断；取值 3 ← 诊断

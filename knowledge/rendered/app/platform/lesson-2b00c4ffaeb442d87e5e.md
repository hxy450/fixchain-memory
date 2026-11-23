# 接入 identifier.getOAID 时同批声明 APP_TRACKING_CONSENT 并在隐私同意后申请；全零串按未授权处理

## 何时使用

服务层实现阶段，把源端 OAID（MSA 或厂商通道）采集迁到鸿蒙 identifier.getOAID 时

## 适用情境

源端在隐私协议同意后静默采集 OAID，写缓存、上送归因接口并发布就绪事件；鸿蒙 getOAID 需要 user_grant 权限 ohos.permission.APP_TRACKING_CONSENT，未授权时返回全零串；Android 端没有对应的运行期授权。

## 例外与边界

- 用户拒绝过 APP_TRACKING_CONSENT 后，再次调用 requestPermissionsFromUser 不会再弹窗；之后的启动照常走全零串（未授权）分支继续，不把申请没成功当作阻塞启动或报错的条件。

## 原因

只换采集 API 而不声明、不申请权限，getOAID 恒返回全零串，归因静默失效；申请时机在源端没有对应行为，需要显式决定。来源中采集 worker 读 d.ts 后发现缺口，但 module.json5 不在其写域，只能记为决策缺口，后一轮才补。

## 做法

1. 在 module.json5 声明 ohos.permission.APP_TRACKING_CONSENT（reason 用各语言目录的 $string，usedScene 指向入口 Ability）；在隐私协议同意门之后 checkAccessToken/requestPermissionsFromUser，再调用 identifier.getOAID；申请不推迟启动门闩，超时兜底照常先行武装。
2. 把返回的全零串视为未授权：记日志并按源端语义继续，不当作有效标识；派工时把 module.json5 与字符串资源一并划入写域。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 2 步〕identifier.getOAID 需要 ohos.permission.APP_TRACKING_CONSENT 权限，没有该权限时得到的 OAID 是 00000000-0000-0000-0000-000000000000
- 〔适用情境 / 做法第 1 步〕ohos.permission.APP_TRACKING_CONSENT 的权限级别是 normal，授权方式是用户授权（user_grant），起始版本 API 9
- 〔做法第 1 步〕在 module.json5 申请 user_grant 权限时，reason 必填并需多语种适配，格式为 $string: ***；usedScene 必填，abilities 填 UIAbility 或 ExtensionAbility 名称的字符串数组，when 只能填 inuse 或 always

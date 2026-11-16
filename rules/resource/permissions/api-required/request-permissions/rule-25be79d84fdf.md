# 接入 getOAID 时在 module.json5 声明追踪权限，带 reason 和 usedScene

审的是：资源
触发（任一种）：
- 读到：目标代码调用 identifier.getOAID()；写错的样子：module.json5 的 requestPermissions 里没有 ohos.permission.APP_TRACKING_CONSENT，或有了但缺 reason（$string 引用）、usedScene，或 reason 的字符串只在 base 没有 en_US
适用范围：目标工程调用 OAID 接口时的 module.json5 和字符串资源
做法：
- requestPermissions 里加 { "name": "ohos.permission.APP_TRACKING_CONSENT", "reason": "$string:<理由键>", "usedScene": { "abilities": ["<使用它的 Ability>"], "when": "inuse" } }，理由文案在 base 和 en_US 的 string.json 里各写一条
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- ohos.permission.APP_TRACKING_CONSENT：权限级别 normal，授权方式 user_grant，起始版本 9：要声明并在运行时向用户申请（出处：permissions-for-all-user.md，ohos.permission.APP_TRACKING_CONSENT）
- reason 申请 user_grant 权限时必填并需多语种适配，格式为 $string: ***：理由要引用字符串资源，并做多语种（出处：declare-permissions.md，在配置文件中声明权限（reason））
- usedScene 申请 user_grant 权限时必填，含 abilities 和 when，when 只能填 inuse 或 always：使用场景两项都要写（出处：declare-permissions.md，在配置文件中声明权限（usedScene））
- 未授权时 getOAID 得到 00000000-0000-0000-0000-000000000000：不声明、不申请就只能拿到全零串（出处：鸿蒙 SDK 的 ets/api/@ohos.identifier.oaid.d.ts，identifier.getOAID）
针对本应用要查的：
- 使用权限的 Ability 名：目标工程 module.json5 的 abilities 列表，找发起采集的 UIAbility；把它的 name 写进 usedScene.abilities
来源：1 张卡，1 个应用
- case-5c6be3ec08184086fd79（DeepAI全能PPT）：做法第 1 步 ← 建议 2

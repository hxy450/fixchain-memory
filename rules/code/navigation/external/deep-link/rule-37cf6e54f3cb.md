# 解析 want.uri 时按源端 uriPattern 锚定整串，不匹配就清空待处理状态

审的是：代码
触发（任一种）：
- 读到：源端 Navigation DeepLink 的 uriPattern 写成 https://<host>/<路径>/{参数}，参数有类型（如数字 id）；写错的样子：onCreate/onNewWant 把 want.uri 交给一个不带 ^…$ 的正则（只匹配 host/路径片段、不含 scheme，或带 /i），匹配不上时不清空上一次的待处理 id
适用范围：目标端在 UIAbility 里把 want.uri 解析成页面路由、并暂存待处理导航的代码
做法：
- 按源端 uriPattern 写全锚定的匹配：^https?://<host>/<路径>/(<参数类型对应的子式，如 \d+>)$，scheme、host、每个路径段和参数类型都锚定
- 匹配不上时把待处理的导航状态清空，让非目标路径停在默认页（列表），不沿用上一次的 id
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- ^https?://<host>/<路径>/(\d+)$，不匹配时清空待处理 id：数字 id 参数的深链在目标端的匹配写法（出处：卡里修好并验证过）
- uri?: string：要解析的链接字符串，可能为空，先判空再匹配（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.Want.d.ts，Want.uri）
针对本应用要查的：
- 源端深链的完整形式和参数类型：源工程里 Navigation 目的地声明的 deepLinks（uriPattern）和该参数声明的类型；清单 <intent-filter> 的 <data> 给出 scheme 和 host；把 uriPattern 里的固定部分照写、{参数} 按参数类型换成子式，两端加 ^ 和 $
未核实：源端参数为数字以外的类型时的子式卡里没给
来源：1 张卡，1 个应用
- case-6bc0c044e9bb2281aa01（Cofi）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4、诊断；取值 1 ← 诊断

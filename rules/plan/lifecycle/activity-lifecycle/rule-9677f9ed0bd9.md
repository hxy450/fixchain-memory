# 源偏好在 Application.onCreate 同步构建时，派工验收要求同步 API 预热，不写异步写队列

审的是：计划与派工
触发（任一种）：
- 读到：源 Application.onCreate 里先同步初始化 SharedPreferences（或 EasyPrefs 等封装），再做其他初始化，此后各处直接读；写错的样子：派工验收标准写「异步初始化容错」「context 未就绪时缓存写队列」，并称这是对齐源端初始化语义
适用范围：派工者为偏好存储封装写任务说明和验收标准时
做法：
- 验收写成「EntryAbility.onCreate 里用 preferences.getPreferencesSync 预热；读用 getSync，写用 putSync / deleteSync / clearSync，写后 flush」
- 按源端真实时序描述：偏好在 Application.onCreate 同步构建、读阻塞到载入完成；不把写队列、异步容错写成对齐语义
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- SharedPreferencesImpl 的各个 get 方法先 awaitLoadedLocked()，未载入完就等待：源端读偏好会阻塞到文件载入完成，不会读到载入前的默认值（出处：android.app.SharedPreferencesImpl#awaitLoadedLocked、#getString）
- function getPreferencesSync(context: Context, options: Options): Preferences：同步取得 Preferences 实例，实例载入文件全部数据并驻留内存（出处：鸿蒙 SDK 的 ets/api/@ohos.data.preferences.d.ts，preferences.getPreferencesSync）
未核实：卡里修好时的目标 SDK 是 6.1.1(24)，本机核实声明用的是 API 23
来源：1 张卡，1 个应用
- case-fb9e44071c44d06a6c71（omni-notes-hmos）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1

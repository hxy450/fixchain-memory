# 源端偏好同步构建时，封装用 getPreferencesSync 和 *Sync 提交，不做异步载入加写队列

审的是：代码
触发（任一种）：
- 读到：源 SharedPreferences 在 Application.onCreate 同步构建，此后各处直接 getBoolean / getString 读；写错的样子：封装用 preferences.getPreferences(...) 异步载入加内存缓存和 pending 写队列，注释写「读取前不阻塞」，就绪前读返回调用方默认值，put / delete / clear 各自异步排队
适用范围：把 SharedPreferences 迁成 @ohos.data.preferences 的偏好封装时
做法：
- EntryAbility.onCreate 里 preferences.getPreferencesSync(context, { name: <文件名> }) 装载，需要内存镜像时用 getAllSync()
- 内存提交用 putSync / deleteSync / clearSync 保证顺序，落盘再异步 flush()
- 若仍用异步 getPreferences，必须写明就绪前读的行为并与源端一致，否则改用同步装载
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- function getPreferencesSync(context: Context, options: Options): Preferences：同步取得实例，载入文件全部数据并驻留内存（出处：鸿蒙 SDK 的 ets/api/@ohos.data.preferences.d.ts，preferences.getPreferencesSync）
- getSync(key: string, defValue: ValueType): ValueType：同步读，找不到或类型不符时返回 defValue（出处：鸿蒙 SDK 的 ets/api/@ohos.data.preferences.d.ts，Preferences.getSync）
- putSync(key: string, value: ValueType): void；deleteSync(key: string): void；clearSync(): void：同族接口：同步写内存，要落盘再调 flush（出处：鸿蒙 SDK 的 ets/api/@ohos.data.preferences.d.ts，Preferences.putSync、deleteSync、clearSync）
- getAllSync(): Object：同族接口：同步取全部键值（出处：鸿蒙 SDK 的 ets/api/@ohos.data.preferences.d.ts，Preferences.getAllSync）
- flush(): Promise<void>：异步把内存里的 Preferences 写到文件（出处：鸿蒙 SDK 的 ets/api/@ohos.data.preferences.d.ts，Preferences.flush）
- 装载改 getPreferencesSync + getAllSync，内存提交改 putSync / deleteSync / clearSync：修好后的写法（出处：卡里修好并验证过）
未核实：卡里修好时的目标 SDK 是 6.1.1(24)，本机核实声明用的是 API 23
来源：1 张卡，1 个应用
- case-fb9e44071c44d06a6c71（omni-notes-hmos）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2、诊断；做法第 3 步 ← 建议 2；取值 6 ← 诊断

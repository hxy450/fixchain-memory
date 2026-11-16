# 同步读设置改成 async load 时，initialize 用 try/catch，失败复位已初始化标志

审的是：代码
触发（任一种）：
- 读到：源端用 SharedPreferences 的 getString / getInt 带默认值同步读设置（Compose 在 remember 里读）；目标端的偏好封装是 async，内部返回 preferences.getPreferences(...) 的 Promise，未就绪时 throw；写错的样子：initialize() 里先写 `this.initialized = true` 再 await 加载，没有 try/catch；加载 reject 时标志不复位，之后再调用直接返回
适用范围：把源端同步读取的设置改成目标端异步加载，并用一次性守卫标志保证只初始化一次的 ViewModel
做法：
- initialize() 写成 try { await 加载; 之后的出题、保存等 } catch (e) { 复位已初始化/进行中标志; throw new Error(...) }，把错误交回调用方
- 只初始化一次的守卫：要么成功后才置 true，要么在 catch 里复位；不要在 await 之前置 true 又不在失败时复位
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- function getPreferences(context: Context, name: string): Promise<Preferences>：取偏好实例是异步的，声明里可抛 BusinessError 401（参数错误）和 15500000（内部错误），所以加载链会 reject（出处：鸿蒙 SDK 的 ets/api/@ohos.data.preferences.d.ts，preferences.getPreferences）
- get(key: string, defValue: ValueType): Promise<ValueType>：读键也是异步的，缺键返回 defValue，同样可抛 15500000（出处：鸿蒙 SDK 的 ets/api/@ohos.data.preferences.d.ts，Preferences.get）
- String getString(String key, @Nullable String defValue)；int getInt(String key, int defValue)：源端是同步读取、缺键返回默认值，没有失败分支；目标端的失败路径是改成异步后新增的（出处：android.content.SharedPreferences#getString、android.content.SharedPreferences#getInt）
- try/catch 包住加载、延时、出题与保存，失败时复位 initialized=false 并抛出错误：按此改后页面可重试（出处：卡里修好并验证过）
- function getPreferences(context: Context, options: Options): Promise<Preferences>：同族接口：按 Options 取偏好实例，同样返回 Promise（出处：鸿蒙 SDK 的 ets/api/@ohos.data.preferences.d.ts，preferences.getPreferences）
来源：1 张卡，1 个应用
- case-346f57800b71b616129f（听音练习）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 4 ← 诊断

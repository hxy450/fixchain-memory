# 偏好读点的缺省值、读取类型和读取时机

agent 会看到什么：读到源端在各处用 getBoolean / getString / getInt(键, 缺省值) 读同一偏好（各读点缺省值不同、传 null 区分缺键、按字符串值域读、在点击回调里现读）；产物里 getSync 的缺省值和类型、有没有 hasSync 判缺键，以及是在回调里现读还是 aboutToAppear 读一次缓存

## 通用查法

### 目标端用 getSync 读偏好时，回源端逐个读点核对缺省值、读取类型和读取时机

审的是：代码
触发（任一种）：
- 读到：源端在多处用 SharedPreferences 的 getBoolean / getString / getInt(键, 缺省值) 读同一个键；写错的样子：目标端 getSync(键, 缺省值) 的缺省值、类型或读取位置是按键常量注释、spec 摘要或某一处读点统一写的，没有逐个读点对照源码
适用范围：安卓 SharedPreferences 的读取迁成 @ohos.data.preferences 的 getSync 时
做法：
- 在源工程里搜这个键的常量名或键名字符串，逐处记下 getX 的方法（读取类型）、第二个参数（缺省值，含 null）和所在的方法或回调（读取时机）
- 目标端每个读点照源端写：getSync(键, 该读点自己的缺省值)，按源端的类型和值域比较；源端在点击等回调里现读的，目标也在同一回调里调 getSync，不复用页面出现时的缓存
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- getSync(key: string, defValue: ValueType): ValueType：缺省值由每次调用传入，键不存在时返回这次调用给的 defValue，所以各读点可以各写各的缺省值（出处：鸿蒙 SDK 的 ets/api/@ohos.data.preferences.d.ts，Preferences.getSync）
- getSync 读到的值为 null 或类型不符时返回 defValue：读取类型和源端不一致时不报错，静默落到缺省值（出处：鸿蒙 SDK 的 ets/api/@ohos.data.preferences.d.ts，Preferences.getSync）
针对本应用要查的：
- 这个键在源端的全部读点：源工程的 Java / Kotlin 文件里搜键常量名或键名字符串，看每处 getBoolean / getString / getInt 调用；逐处记下读点所在的方法或回调、读取类型和第二个参数的缺省值；缺省值不同的读点分别保留
- 字符串偏好的取值集合：设置页偏好 XML 里对应 ListPreference 的 entryValues，或键常量旁的注释；读出取值集合，目标端按同样的字符串值比较，不改读成布尔
来源：3 张卡，2 个应用
- case-91084f18203ecc5e7036（opencamera-hmos）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3
- case-a293ed8cf3fa860f8330（omni-notes-hmos）：做法第 2 步 ← 建议 4
- case-fb9e44071c44d06a6c71（omni-notes-hmos）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3

## 规矩

- rule-3ee794727d2e｜同一偏好键在不同读点缺省值不同时，各读点保留自己的显式缺省值，不收敛成单一默认｜读到：源码同一偏好键在不同读点用不同缺省值（如一处 getBoolean(key, false)、另一处 getBoolean(key, true)），或键表写「读点不一致 / 该读点特判」；写错：键常量注释只留一个默认值，封装只提供以该默认值读取的单一访问器（如只有 getSync(<键>, false)）
- rule-b16330d50d2f｜改某个偏好读点的缺省值前回到该读点的源码行核对，不按 spec 摘要或键常量的单一默认改｜读到：spec 摘要或键常量注释给这个偏好键只写一个默认值（如 `(boolean, false)`），页面已有的读点按另一个缺省值读（如 getSync(<键>, true)）；写错：原本 getSync(<键>, true) 的读点被改成按 false 读，注释引键常量或 spec 摘要里的单一默认
- rule-e0ef9bf397f2｜源端用 getString(key, null) 区分缺键而空串合法时，目标用 hasSync 判缺键，不拿空串当哨兵｜读到：源端 SharedPreferences 的 getString(key, null)，只在返回 null 时跳过，空串是合法值；写错：目标读偏好写成 getString(key, '') 或 getSync(key, '')，再跳过 === '' 的项，注释里写「空串丢失已接受」
- rule-f7d2ab9c942d｜接线组装保存请求时打开源方法逐字段对照：偏好类型、格式映射、有效性门控｜读到：源端在一个方法里用 sharedPreferences.getString(...) 读多项偏好（含 no / photo 这类字符串值域、图片格式、按模式区分的存底偏好），并按传感器数据是否有效的标志决定写不写方位、俯仰角；写错：目标把字符串偏好读成 getBoolean(..., true)，请求的格式字段不赋值走默认，模式相关的存底偏好不映射；方位、俯仰写死 0 并注释「公开面未导出」，不查有效性标志；注释引用的源码区间不是这段逻辑
- rule-cd6648370e03｜源端在点击时实时读首选项的判定，目标端也在回调里现读，不在 aboutToAppear 缓存｜读到：点击监听里实时调用首选项的 `getString(key, null)`，按是否为 null 判定先走哪条分支；写错：`aboutToAppear` 里读一次存进 `@Local` 字段，点击回调直接用这个字段判定

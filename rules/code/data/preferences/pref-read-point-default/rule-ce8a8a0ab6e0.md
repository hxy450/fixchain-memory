# 目标端用 getSync 读偏好时，回源端逐个读点核对缺省值、读取类型和读取时机

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

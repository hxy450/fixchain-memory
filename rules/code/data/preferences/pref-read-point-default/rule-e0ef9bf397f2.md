# 源端用 getString(key, null) 区分缺键而空串合法时，目标用 hasSync 判缺键，不拿空串当哨兵

审的是：代码
触发（任一种）：
- 读到：源端 SharedPreferences 的 getString(key, null)，只在返回 null 时跳过，空串是合法值；写错的样子：目标读偏好写成 getString(key, '') 或 getSync(key, '')，再跳过 === '' 的项，注释里写「空串丢失已接受」
适用范围：迁移以 null 区分缺键的偏好读取、且空串本身是合法取值时
做法：
- 先用 Preferences.hasSync(key)（或给偏好封装补一个 has/hasSync）判断键是否存在，存在时再取值，空串照常保留
- 偏好封装暂时补不了 has 时，把它登记为待裁定的契约缺口，不在注释里自行接受数据丢失
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- String getString(String key, @Nullable String defValue)：键存在时返回值，否则返回 defValue：源端传 null 作默认值，就是用 null 表示缺键（出处：android.content.SharedPreferences#getString）
- hasSync(key: string): boolean：Preferences 里有没有这个键（出处：鸿蒙 SDK 的 ets/api/@ohos.data.preferences.d.ts，Preferences.hasSync）
- getSync(key: string, defValue: ValueType): ValueType：值为 null 或类型不符时返回 defValue：只用 getSync 的默认值区分不了缺键和合法空串（出处：鸿蒙 SDK 的 ets/api/@ohos.data.preferences.d.ts，Preferences.getSync）
- has(key: string): Promise<boolean>：同族接口：Preferences 的异步版本（出处：鸿蒙 SDK 的 ets/api/@ohos.data.preferences.d.ts，Preferences.has）
- 偏好封装新增 hasKey，历史读取按键存在性保留空串：卡里的修法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-bebaba79e02c02cca6a1（opencamera-hmos）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4；取值 5 ← 诊断

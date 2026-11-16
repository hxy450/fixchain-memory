# 拦截器读取的公参键在工程里没有写入点时，按源端来源补生产者

审的是：代码
触发（任一种）：
- 读到：源端隐私同意后的 initSdk 序列里有 OAIDHelper.getOAID 等获取设备标识的步骤，网络公参取的就是这些值；写错的样子：目标的公参 provider / Interceptor 只从偏好键读 oaid 这类字段，工程里没有任何代码写这个键；隐私后初始化链里没有 OAID 步骤
适用范围：迁移网络公共参数、改写隐私同意后的初始化链时，拦截器读取的每个本地键
做法：
- 对拦截器读取的每个本地键在目标工程里检索写入点；把源端 initSdk 的步骤逐项对到目标 initializer，每个字段都要有获取并写缓存的生产者，找不到来源的登记为缺口
- oaid：在隐私同意后的初始化里先做 OAID 的获取并写入公参读取的那个键，再创建公参 provider；module.json5 的 requestPermissions 里声明 ohos.permission.APP_TRACKING_CONSENT
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 获取 OAID 要 ohos.permission.APP_TRACKING_CONSENT，否则得到 00000000-0000-0000-0000-000000000000：不声明权限时 oaid 字段是全零（出处：鸿蒙 SDK 的 ets/api/@ohos.identifier.oaid.d.ts，identifier.getOAID）
- 隐私后初始化里先初始化 OAID 获取、再创建公参 provider，并声明 APP_TRACKING_CONSENT：修复后 oaid 公参有值（出处：卡里修好并验证过）
针对本应用要查的：
- 每个公参字段在源端由谁写入：源工程 Application 的隐私同意后初始化方法（如 initSdk）和各 SDK 封装类；目标工程里按偏好键名全文搜写入调用；只搜到读取、没有写入的键，就照源端那一步（获取来源、隐私门禁、所需权限）补生产者
未核实：卡里记的环境没写鸿蒙 SDK 版本，本机按 API 23 的声明核实
来源：1 张卡，1 个应用
- case-24bba18989317118cb97（记得日历）：做法第 1 步 ← 建议 1、建议 2；做法第 2 步 ← 诊断、建议 2；取值 2 ← 诊断

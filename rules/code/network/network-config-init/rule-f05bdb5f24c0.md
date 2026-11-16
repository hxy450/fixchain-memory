# 源端 baseUrl 由注入带上、目标改显式 init 时，在 EntryAbility.onCreate 调它

审的是：代码
触发（任一种）：
- 读到：源端 Retrofit.Builder().baseUrl(...) 在 Hilt 模块的 @Provides 方法里注入时带上，Application.onCreate 里没有网络初始化调用；写错的样子：目标网络层的 baseUrl 默认空串、只在 init() 里赋值，但 EntryAbility.onCreate 里没有调用这个 init()，或者只在业务服务（如环境切换）里调用
- 写错的样子：冷启动就发请求的流程（如闪屏静默游客登录）只做了 token 加载就发请求，EntryAbility.onCreate 里没有先完成网络 init()
适用范围：源端网络配置靠依赖注入在构造实例时带上、目标端改成静态客户端加需显式调用的初始化入口时
做法：
- 在 EntryAbility 里 import 网络层的初始化入口，onCreate 开头写 await <初始化入口>()，早于任何请求；和实现初始化入口放在同一个任务里完成
- 写冷启动即发请求的流程前，确认上一步已在 onCreate 里完成；只加载 token 不等于网络层就绪
- 在 entry/src/main/ets 下搜初始化入口的调用（如 grep -rn "\.init("），命中要落在 EntryAbility 的 onCreate；只命中业务服务的按未接线处理
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): void：UIAbility 冷启动时的初始化回调；声明写明它同步返回、不支持异步回调（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.UIAbility.d.ts，UIAbility.onCreate）
- 修复是在 EntryAbility 里引入初始化入口，并在 onCreate 开头 await 它，保留到观察截止：修复后的接线位置；修复前请求因 baseUrl 为空发成没有 https:// 和 host 的相对路径（出处：卡里修好并验证过）
针对本应用要查的：
- 目标网络层的初始化入口叫什么、是否异步：目标工程网络层目录里给 baseUrl 赋值的那个静态方法，注释里常写「应用启动时初始化」「由 EntryAbility 初始化」；读出方法名和返回类型；返回 Promise 的在 onCreate 里 await 它
未核实：卡里的行为出自 API 22（6.0.2），声明按本机 API 23 核对；onCreate 声明为同步返回，await 初始化之后的页面加载是否一定晚于初始化完成，卡里没有单独核对
来源：1 张卡，1 个应用
- case-8555b02fdd531952938b（polypal-app-ohos）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 4；做法第 3 步 ← 建议 3；取值 2 ← 诊断

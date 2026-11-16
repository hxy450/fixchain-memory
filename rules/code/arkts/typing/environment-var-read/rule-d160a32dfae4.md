# getEnvironmentVar 读可选配置时，先兜空串再读 .length 或做 Number()

审的是：代码
触发（任一种）：
- 读到：改写前的代码是 `process.getEnvironmentVar('X') || ''` 这类带缺省的回退链；写错的样子：改成 `const v = process.getEnvironmentVar('X')` 后直接读 `v.length` 或 `Number(v)`，没有 `|| ''` / `?? ''` 或判 undefined
适用范围：ArkTS 代码用 getEnvironmentVar 读成功码、密钥、渠道、客户端身份等可选运行配置时
做法：
- 写成 const v: string = process.getEnvironmentVar('X') ?? ''（或 || ''，或先判 v === undefined），之后再读 v.length、做 Number(v)
- 环境变量读取收敛到一个返回 string 的函数（内部兜 undefined），各配置方法都调它；改了一项，其余同形配置项按同一写法核对
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- getEnvironmentVar(name: string): string（ProcessManager，@since 11 的写法）：声明的返回类型只写 string，看不出可能是 undefined（出处：鸿蒙 SDK 的 ets/api/@ohos.process.d.ts，ProcessManager.getEnvironmentVar）
- 如果环境变量不存在，返回 undefined：变量缺失时的返回值，取值前必须兜空（出处：js-apis-process.md，getEnvironmentVar9+）
- function getEnvironmentVar(name: string): string，@deprecated since 9，@useinstead ohos.process.ProcessManager.getEnvironmentVar：同族接口：模块级的 process.getEnvironmentVar，已废弃（出处：鸿蒙 SDK 的 ets/api/@ohos.process.d.ts，process.getEnvironmentVar）
- 安装后的 HAP 进程环境里没有构建期的这些变量；去掉 || '' 后读 .length 报 Cannot read property length of undefined，恢复后通过：变量缺失是真机上的常态分支（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-2cb47bb8a097227ee9cf（app_hnaccurateweather_live_android）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1、建议 2；取值 4 ← 诊断

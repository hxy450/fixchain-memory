# 源码对 Toast 文案做 toLowerCase 等加工时，getStringSync 取成 string 后照样加工

审的是：代码
触发（任一种）：
- 读到：源码 Toast 文案先 getString(R.string.…) 再 .toLowerCase() 等字符串加工后拼接；写错的样子：目标已用 resourceManager.getStringSync(...) 把资源取成 string，却删掉了 .toLowerCase()，直接用资源原文拼接
适用范围：源端对资源字符串做了加工（大小写、截取、拼接等）后再显示时
做法：
- 先用 getStringSync($r('app.string.<键>')) 或 getStringSync(<资源 id>) 取得 string，再照源码保留加工（如 .toLowerCase()），按源码顺序拼接
- 以平台限制为由删掉源码加工前，先查实际用的 API 返回类型；返回 string 的不能套 Resource 层面的限制
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- getStringSync(resource: Resource): string：ResourceManager 按 Resource 取字符串，返回的是 string，可以直接 toLowerCase（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，ResourceManager.getStringSync）
- getStringSync(resId: number): string：同族接口：按资源 id 取字符串（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，ResourceManager.getStringSync）
- getStringSync(resource: Resource, ...args: Array<string | number>): string：同族接口：带格式化参数的取法（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，ResourceManager.getStringSync）
来源：1 张卡，1 个应用
- case-65c33c4172d6d208c5a5（MifareClassicTool）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3

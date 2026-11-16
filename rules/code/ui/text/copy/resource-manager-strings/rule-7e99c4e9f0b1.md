# HAR 页面把按名取资源改写成静态 $r 时，先确认名字在本模块或已声明依赖里

审的是：代码
触发（任一种）：
- 读到：HAR 页面用 `getStringByNameSync(name)` 或封装的按名取字符串函数取文案；写错的样子：改写成 `$r('app.string.X')`，而 X 只在壳模块、AppScope 或未依赖的模块里定义
适用范围：在 HAR 页面内把按名取资源改写为静态 $r 时
做法：
- 每个名字先确认在本模块或 oh-package.json5 声明的依赖里存在；只在壳、AppScope 或未依赖模块里的，按本模块命名建立三语（base、zh_CN、en_US）自有资源，再写 $r('app.string.<本模块的名字>')
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- getStringByNameSync(resName: string): string：运行时按名取字符串，在整包合并后的资源里找，所以壳里的名字也能取到（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，ResourceManager.getStringByNameSync）
- getMediaByNameSync(resName: string, density?: number): Uint8Array：同族接口：按名取媒体，改写成 $r('app.media.X') 时同样要先核名字归属（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，ResourceManager.getMediaByNameSync）
- 改用本模块自有名字并补齐 base/zh_CN/en_US 三语，壳里的原名留给壳里的页面：修复后的做法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-e218dc5f282b590164d7（记得日历）：做法第 1 步 ← 建议 4、诊断；取值 3 ← 诊断

# 有应用内语言切换时，resourceManager 取串、数组、复数、颜色一律传 $r(...).id

审的是：代码
触发（任一种）：
- 读到：工程用 i18n.System.setAppPreferredLanguage 做应用内语言切换，既有取串辅助写成 resourceManager.getStringSync(res.id)；写错的样子：新写的取值传 Resource 对象：getStringArrayValue($r('app.strarray.…'))、getStringSync(resource)、getColorSync($r('app.color.…'))，没带 .id
适用范围：目标工程实现了 setAppPreferredLanguage 应用内语言切换，用 context.resourceManager 同步取字符串、字符串数组、复数串或颜色时
做法：
- 一律用 number 重载：resourceManager.getStringSync($r('app.string.x').id, ...args)；getStringArrayValue(Sync)、getIntPluralStringValueSync、getColorSync 同样传 $r(...).id
- 写新文件或新辅助函数前照搬工程既有取串辅助的 .id 写法，并推及数组、复数、颜色等所有取值方法；用脚本批量改写后搜一遍不带 .id 的调用
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- getStringSync(resId: number, ...args: Array<string | number>): string：ResourceManager 按资源 id 取字符串（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，ResourceManager.getStringSync）
- getStringSync(resource: Resource, ...args: Array<string | number>): string，@deprecated since 20，@useinstead ohos.resourceManager.getStringSync：Resource 对象重载自 API 20 起废弃；数组、复数、颜色的 Resource 重载同样标了废弃（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，ResourceManager.getStringSync）
- getStringArrayValueSync(resId: number): Array<string>；getStringArrayValue(resId: number): Promise<Array<string>>：同族接口：按 id 取字符串数组（同步、Promise）（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，ResourceManager.getStringArrayValueSync、ResourceManager.getStringArrayValue）
- getIntPluralStringValueSync(resId: number, num: number, ...args: Array<string | number>): string：同族接口：按 id 取复数串（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，ResourceManager.getIntPluralStringValueSync）
- getColorSync(resId: number): number：同族接口：按 id 取颜色（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，ResourceManager.getColorSync）
- setAppPreferredLanguage 设置后，应用优先加载应用偏好语言对应的资源：应用内语言切换依赖它，取资源的写法要能跟上这个偏好（出处：js-apis-i18n.md，setAppPreferredLanguage）
- Resource 对象重载取到的串不随应用偏好语言，改成 .id 重载后中文界面不再混入英文：两种重载的语言解析差异是返修实测得出的（出处：卡里修好并验证过）
未核实：Resource 重载不随应用偏好语言是返修实测推断，文档和声明里没写这一差异；卡里环境是 API 24（6.1.1），本机按 API 23 的声明核对
来源：1 张卡，1 个应用
- case-e5f37ee4dce62e2a89c2（omni-notes-hmos）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1、建议 2；取值 7 ← 诊断

# 代码里用 getStringSync 取成字符串的文案，语言运行期切换时在同页配置变化回调里重取

审的是：代码
触发（任一种）：
- 读到：源端在组合期取串拼接运行时值（如 stringResource(R.string.x) + BuildConfig.VERSION_NAME），切换语言靠 Activity recreate 后按新语言重取；写错的样子：页面在 aboutToAppear 里 resourceManager.getStringSync($r('app.string.x').id) 取一次存进 @Local / @State 或作 string 参数下传，配置变化回调里没有重取
适用范围：目标页面在运行期切换语言时不重建，文案在代码里取成字符串而不是在渲染期用 $r 时
做法：
- 把取值函数挂到本页的配置变化通知上重取（如应用转发的配置重放事件回调末尾再调一次取值函数），或改为在渲染期取值；不把它算进「$r 自动重解析」
- 接线配置重放的页面订阅时，检索本页 resourceManager 取值后写进状态的调用，与重放清单对账；按新配置重读源端会重读的文案，不算「源端没有的复位」
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 语言切换后 $r 渲染的文本自动刷新，getStringSync 取得并存入状态的文案保持旧值；在配置重放回调末尾再调取值函数后中英双向切换都正确：两种取值方式的差别和修复（出处：卡里修好并验证过）
- getStringSync(resId: number): string；getStringSync(resource: Resource): string：按调用时的配置取一次字符串（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，resourceManager.ResourceManager.getStringSync）
- onConfigurationUpdate(newConfig: Configuration): void：系统配置更新时调用：语言等配置变化的入口，页面通常经应用内事件转发拿到（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.Ability.d.ts，Ability.onConfigurationUpdate）
来源：1 张卡，1 个应用
- case-780845d2d4ab2eae2a15（GameOfLife）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 4；取值 1 ← 诊断

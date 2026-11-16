# Activity 壳层经 setContent 下传的设置和派生结果

agent 会看到什么：读到源 Activity 在 setContent 里从设置存储读出设置、或在顶层算出派生结果（如 设置.toEnum<…>().isActive(…)），作为 Composable 参数下传各路由，同文件 @Preview 另给示例实参；产物里页面另存一块本地设置字段、取 @Preview 的实参当初值、只在 aboutToAppear 取一次快照，或各页自己写 !== 0 / === 1 重算

## 规矩

- rule-a0a878deed15｜设置类字段直接读设置存储的实时值，页面不另存一套本地副本｜读到：源端设置由 Activity 从设置存储读出、作为 Composable 参数下传；写错：页面里有一整块本地设置字段，只在 aboutToAppear 取一次快照，或照抄兄弟页的字段块和判断式
- rule-5507565bae8f｜调用方注入的必填设置参数，接线前的占位初值取源端默认值常量，不取 @Preview 示例实参｜读到：源 Composable 的设置参数没有默认值、由调用方（Activity 壳层）下传，同文件 @Preview 函数里另给了一组示例实参；写错：目标页面的本地设置字段照搬 @Preview 的示例实参，注释写「接线前取 Android 默认」
- rule-e2aabebf970c｜源端在壳层算一次再下传的派生结果，目标端也在壳层算一次放进全局状态｜读到：源 Activity 的 setContent 顶层算出派生结果（如 设置.toEnum<枚举>().isActive(connectivityManager)），再作参数下传各路由；写错：各页自己写 settings.x !== 0、> 0、=== 1 重算；或入口页私有函数算出结果却不提供给页面

# 照源码移植的 Service、Repository 和 Dao 调用

agent 会看到什么：读到源端 Service / ViewModel 经 Repository、Dao 的调用（分阶段的缓存读写、@Body 请求体的组装、按多个键的查询）；产物里移植后的方法少了调用、参数或字段：漏掉某阶段的副作用、写方法没有调用者、body 写成 {}、少了月份键

## 规矩

- rule-635353318897｜把源端服务流程内联移植到目标方法时，逐阶段落齐源函数的全部副作用调用｜读到：源端 Service 的扫描方法分阶段执行：开头读缓存做预过滤，收尾在保存结果、置偏好标记之前还调用 Repository 的缓存更新方法；写错：目标方法只移植了结果持久化和偏好标记，Repository 的缓存更新调用和开头的缓存预过滤都没有；文件头的「对齐源端各阶段」流程说明也漏列这两步
- rule-63268014275f｜照源码移植的 Repository / DAO 写方法没有调用者时，回查源流程哪一步该调用它｜读到：源端流程里有对 Repository / DAO 写方法的调用；写错：目标里定义了照源码移植的 Repository / DAO 写方法（注释写「对齐 …」），在目标工程里 grep 不到调用者
- rule-0ea907adb490｜Service 只收不透明请求体时，Repository 照源端构造处逐项写 body，不写 {} 占位｜读到：源端 Service 方法参数是 `@Body ... RequestBody`，请求体在调用它的 Repository 方法里组装；目标 Service 方法只收 `data: Object` 原样 POST；写错：Repository 里写成 `const body: Record<string, Object> = {}` 直接传给只收 `data: Object` 的 Service 方法，源端组装的字段一个都没有
- rule-a9dd5c0c1067｜源端实体按月份和分类关联时，目标模型和仓储方法也带月份键并按选中月份读写｜读到：源端实体的构造参数里有月份时间戳和分类键，ViewModel 经 Dao 按（月份时间戳, 分类键）两个参数查询，已有当月记录时按该记录更新；写错：目标模型只加一个数值字段（注释写「每月」却没有月份字段），仓储和服务的方法写成 `set…(id, value)` 不带月份参数，页面读写不按当前选中月份过滤

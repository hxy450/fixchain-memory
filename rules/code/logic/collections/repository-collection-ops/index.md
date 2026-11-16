# 仓库和数据源方法里的集合筛选、排序

agent 会看到什么：读到源端仓库或 ViewModel 的数据源方法对集合做 filter、sortedBy、shuffled、groupBy，或规格按状态集合取数；交回的代码换成日期比较加 slice、写死固定顺序的常量，或登记 FWD-REF 了事

## 规矩

- rule-6ed704c9969c｜仓库聚合方法按规格的状态集合取数据，不用日期比较近似、不另截条数｜读到：规格写聚合结果按状态集合取（如「即将开始与进行中」），待办按所属项分组成 Map；写错：仓库聚合方法用 startDate >= today 一类日期比较过滤再 slice(0, N)，进行中的被排除；待办汇总全部而不按所属项分组
- rule-f77c6c8b0fde｜数据源只是对本地静态集合做 shuffled/filter/sort 时，在组件初始化处直接复现，不登记前向占位｜读到：源端 ViewModel 的数据源方法只是对本地静态种子做 shuffled() / filter / sort（如 exampleLists.shuffled().toMutableList()）；写错：目标把种子照录成固定顺序的常量数组，写一个 `FWD-REF` 标记，理由是「ViewModel 等价体未建」
- rule-bf58c3add349｜源端队列选取不过滤状态时，目标端待推送选取同时取 pending 与 fail｜读到：源端待推送队列的查询只有 equal(…) 按资源类型一个条件、不按同步状态过滤，失败项置 fail 后留在队列里；写错：目标端待推送阶段只查状态为 `'pending'` 的记录，fail 项不再被选中
- rule-5393aa5e75f3｜Kotlin 先 mapNotNull 再 groupBy、maxWith 的管道，ArkTS 保持先过滤后选优｜读到：源码里 `mapNotNull { … }` 或 `filter { … }` 剔除不完整的项，之后 `groupBy { … }` 分组，再用 `maxWith` 或自定义的选优函数挑最佳；写错：ArkTS 里先在全部候选上比较出最佳（循环取最大下标或 `reduce`），之后才做完整性检查，最佳那项不完整就把整组丢弃

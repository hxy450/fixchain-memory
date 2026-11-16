# 集合与顺序

源端有 HashSet / HashMap 遍历、addAll、按下标赋值、按引用原地改写数组、filter / sortedBy / Comparator 排序，目标端有 Set、Map、find、slice、.sort 时

## 触发族

- [仓库和数据源方法里的集合筛选、排序](repository-collection-ops/index.md)（4 条）：读到源端仓库或 ViewModel 的数据源方法对集合做 filter、sortedBy、shuffled、groupBy，或规格按状态集合取数；交回的代码换成日期比较加 slice、写死固定顺序的常量，或登记 FWD-REF 了事
- [列表排序的 Comparator 和排序偏好](list-sort-comparator/index.md)（2 条）：读到源端列表用自己的 Comparator 在 Collections.sort / List.sort 里排序、或排序时读 SharedPreferences 里的排序偏好，产物里是查询结果上的 .sort(比较函数) 和排序配置的读取
- [Java 集合的遍历顺序和入队语义](java-collection-order/index.md)（5 条）：读过的 Java 源码用 HashSet / HashMap 遍历决定输出顺序，或用 List.addAll 整批入队、不去重不设上限；交回的代码改成 Set / Map 的插入序，或加了去重、截断
- [按下标给列表项赋值](index-based-assign/index.md)（1 条）：读过的源码按 indices / forEachIndexed 把常量数组第 i 项赋给列表第 i 项；交回的代码改成 find( 按字段 === 键查找，键缺失时全落空
- [按引用原地改写的数组参数](array-in-place-mutation/index.md)（2 条）：读到源码把调用方传入的 String[] 等数组按引用原地改写（arr[i] = …，改动写回调用方持有的数组）；产物里调用时传 arr.slice() 副本，或服务另存一份副本

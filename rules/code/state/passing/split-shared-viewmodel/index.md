# 共享 ViewModel 拆成页面实例后的状态下传

agent 会看到什么：读到经 AppStorageV2.connect 由各页 getInstance() 共用的 ViewModel；产物里改成各页 new ViewModel()，跨页的筛选状态靠 @Param + @Monitor 或显式传参下传

## 规矩

- rule-c94aea280e58｜拆 AppStorageV2 共享 VM 改各页 new 时，跨页状态改用 @Param+@Monitor 下传｜读到：被拆的 ViewModel 经 AppStorageV2.connect 同一个 key 由各页 getInstance() 共用；其中的 @Trace 状态字段由某一页的动作写入，其他页只读（含查询时隐式读取）；写错：各调用处把 getInstance() 机械替换成 new 出来的 ViewModel 实例，读取页没有新增对应的 @Param + @Monitor，也没有订阅事件；写入动作只改了写入页自己的私有实例
- rule-a94f52a51d22｜VM 改成页面实例后，隐式读 VM 筛选字段的查询要在查询前同步或改成显式传参｜读到：页面调用 VM 的查询方法只传起止时间、不传筛选参数，筛选条件取自 VM 自己的 @Trace 字段；写错：VM 改成页面 new 的实例后，查询前没有把页面当前的筛选值（父页传入的 @Param）写进 VM 字段，也没有改成显式传参；页面虽有对应 @Param，查询仍用 VM 初始化时的值
- rule-d2d84b574049｜新建筛选值下传通道时沿用源头对「全部」哨兵的归一化，不下传条目原始 ID｜读到：VM 的 @Trace 筛选字段在选择动作和偏好读取里都把「全部」类条目归一化成空字符串 ID；写错：新加的 @Param 下传或对 VM 字段的直接赋值，把选择条目或页头保存的原始 ID 原样传下去；「全部」条目的非空 ID 成了过滤条件，选「全部」反而无数据
- rule-768b78a8b45d｜新加 @Monitor 触发重查后，同一次切换不再另外递增刷新计数｜写错：新加的 @Monitor 监听筛选参数并重新查询，同一次切换的关闭回调里又递增刷新计数（revision 一类的 ++），一次切换刷新两轮

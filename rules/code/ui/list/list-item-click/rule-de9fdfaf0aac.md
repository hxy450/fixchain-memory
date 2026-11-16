# 列表行的远端提交按钮按条目 ID 维护在途集合，在途时显示加载态、不再发请求

审的是：代码
触发（任一种）：
- 读到：源端 Adapter 里每行的按钮调用远端接口，成功后只改当前 bean 的字段再 `notifyDataSetChanged()`；写错的样子：目标端点击处理只在「已完成」标记为真时才返回，请求在途时可重复提交；同页别的按钮已有 busy 锁，这个按钮的 `onClick` 没沿用
适用范围：列表每行带调用远端接口的提交按钮（如加入、关注）时
做法：
- 页面维护在途集合（如 @State inFlightIds: string[] 或 Set），发请求前 if (已含 id) return 再加入；成功和失败（finally）都移除
- 在途期间按钮显示加载文案、不响应点击；ForEach / LazyForEach 的 keyGenerator 把在途状态拼进 key，让该行重绘
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 加架增加按 ID 的在途锁、加载中状态和失败释放，列表 key 纳入在途状态：修好的写法（出处：卡里修好并验证过）
- (arr: Array<any>, itemGenerator: (item: any, index: number) => void, keyGenerator?: (item: any, index: number) => string): ForEachAttribute：ForEach 的 keyGenerator 决定每行的 key（出处：鸿蒙 SDK 的 ets/component/for_each.d.ts，ForEachInterface）
- (dataSource: IDataSource, itemGenerator: (item: any, index: number) => void, keyGenerator?: (item: any, index: number) => string): LazyForEachAttribute：同族接口：LazyForEach 同样用 keyGenerator 定 key（出处：鸿蒙 SDK 的 ets/component/lazy_for_each.d.ts，LazyForEachInterface）
- 键值变化时框架视为该元素已被替换，基于新键值创建新组件：把在途状态拼进 key 能让该行重绘（出处：arkts-rendering-control-foreach.md，键值生成规则）
未核实：重复提交是代码核查推断，卡里没有实测到重复请求；安卓源端同样没有显式加锁
来源：1 张卡，1 个应用
- case-7a220ef3945d95389ab4（刺猬猫阅读）：做法第 1 步 ← 建议 3、建议 2；做法第 2 步 ← 建议 3；取值 1 ← 诊断

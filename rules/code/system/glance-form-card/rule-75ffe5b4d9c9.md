# V1 卡片页的派生值写成 build 里调用的普通方法，不写 struct 的 get 访问器

审的是：代码
触发（任一种）：
- 写错的样子：卡片页的 @Entry / @Component struct 里写了 `get` 访问器，build 里不带括号地按属性读它
适用范围：ArkTS 服务卡片里用 V1 状态管理（@Entry、@LocalStorageProp）的卡片页
做法：
- 把访问器改成普通方法：struct 里写「名字(): 类型 { … }」，build 里写 this.名字() 调用
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- V1 卡片页 struct 的 get 访问器在转译产物里不存在，读它恒为 undefined；改成普通方法后保留：用 getter 派生形态时卡片总走同一个分支（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-77c6596fcdf362f9e832（Jetsnack）：做法第 1 步 ← 建议 3、诊断；取值 1 ← 诊断

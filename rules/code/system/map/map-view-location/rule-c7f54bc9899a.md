# 规格要求真实地图且没计划占位时，不能把 Unavailable 适配器当唯一实现

审的是：代码
触发（任一种）：
- 读到：规格要求页面初始化地图、添加 marker、移动相机、点击逆地理编码（API 候选为 AMap 地图 SDK），计划 placeholders_planned 为空；写错的样子：能力注册表默认且唯一的地图实现是 Unavailable 适配器（initialize 恒返回 Unavailable），页面的地图区是灰底 Stack 或「暂无数据」，没有 marker / polyline 模型
适用范围：核心功能依赖厂商地图、POI、导航 SDK，计划为它指定了适配 skill 且没有计划占位时
做法：
- 先读计划指定的适配 skill，接入真实 SDK，注册真实的地图和导航适配器，页面放真实地图组件并补 marker / polyline 模型
- Unavailable 适配器只留作 Key 缺失时的运行期回退：Key 缺失才返回 Unavailable
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 接入 @amap map3d/search/navi 11.2.0，隐私同意后初始化并注册真实适配器，地图视图替换各页灰色占位，补 marker/polyline 模型，Unavailable 适配器保留为 Key 缺失时的回退：返修后的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-ac823e7436e1b08612ba（实时公交）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3、诊断；取值 1 ← 诊断

# 结果每次整体重建、条目是普通 class 时，ForEach 键加每次计算的代次前缀

审的是：代码
触发（任一种）：
- 读到：源端每次计算先 removeAllViews() 再整体重建结果区；写错的样子：渲染模型是普通 class（没有 @ObservedV2 / @Trace），ForEach 的键不含代次，两次计算的条目键相同时复用旧行、显示旧数据
适用范围：目标端结果列表每次计算整体替换、而条目对象不是可观察类时
做法：
- 在产出结果的服务里放一个 generation 计数，每次构建结果时递增，写进条目 key：`${generation}_${分组号}` / `${generation}_${分组号}_${序号}`
- 页面各层 ForEach 都用 item.key 作 keyGenerator
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 模型加 key 字段 + 服务里 generation 每次构建递增，键为「代次_分组[_序号]」，两层 ForEach 用 item.key：修好后验证过的写法（出处：卡里修好并验证过）
- 非首次渲染时键值已存在就不新建组件，直接渲染该键值对应的组件：键不变时旧行被复用，所以整体重建要换键（出处：arkts-rendering-control-foreach.md，非首次渲染）
来源：1 张卡，1 个应用
- case-74bcab538b062ee7cac8（MifareClassicTool）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 诊断；取值 1 ← 诊断

# 源端 factory 按 type 分派 Fragment 时，目标列表收全各 type、保持顺序，不按 type 过滤

审的是：代码
触发（任一种）：
- 读到：源码把配置里的编辑项列表逐项交给 factory，按 type.name 分派到各自的 Fragment（when 分支），没有「须先选中某项」之类前置条件；写错的样子：目标的列表提供函数里写了 .filter(item => item.type !== '<某 type>' && …)，或只在某个选中状态下放行该 type，把它挪给页内另一个入口承载
适用范围：把安卓按配置列表动态生成编辑项（factory 按 type 创建 Fragment）的页面迁成 ArkUI 列表时
做法：
- 列表提供函数只按源端同样的条件筛（如 item.visible && item.supported），每个受支持的 type 都按源端 factory 进列表、保持配置顺序，各自分派到对应页面
- 确要改由目标端已有入口承载某个 type 时，先在决策台账记这条替代决策；台账里没有的，删掉按 type 的过滤
针对本应用要查的：
- 源端列表对编辑项的筛选条件和顺序：源工程里按 type 创建 Fragment 的 factory 类，以及调用它、遍历配置列表的那段代码；读出哪些条件会跳过某项（显隐、是否支持），目标只照这些条件筛，顺序按配置列表
来源：1 张卡，1 个应用
- case-625eea78c41ac46eb931（组件岛Widget Island）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1

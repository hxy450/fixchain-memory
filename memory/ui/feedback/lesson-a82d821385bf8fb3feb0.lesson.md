# 页面由多个数据来源组成、源端各来源只在成功时更新自己的区块时，目标按区块保存结果与错误，局部失败不升级为整页错误

ID：`lesson-a82d821385bf8fb3feb0` · 版本：4

[本主题](index.md)

## 何时使用

界面转换与数据接线阶段，为由多个数据来源（多个接口、首页缓存、本地登录态、XML 静态默认内容）组成的页面设计加载、失败与降级状态，或把 ViewModel 的错误状态绑定到整页错误态时

## 适用情境

源页面的多个请求各自 launch/observe、只在成功时更新自己的数据；或先用缓存填充再请求详情；或首屏含 XML 静态默认文案与本地状态；或列表页的次级动作（定位、权限、选择）失败只给提示。目标准备用一个结果对象、CONTENT/ERROR 两态或单一错误信息字段驱动整页，加载失败时清空已成功的列表，或刷新时用全屏遮罩盖住其他分区。

## 例外与边界

- 缺少城市、参数等所有区块都依赖的前置条件，此时整页错误态是合理的
- 源端失败分支本身清空数据或切到整页错误（如 catch 里置空列表、显示全屏错误页）时照源端实现，不套用保留旧值

## 原因

把多个来源聚合成一个成功/失败判定，任一来源或次级动作失败，就会把已渲染、仍然有效的区块替换成错误或清空；源端“失败不动已有数据”的语义和缓存优先的降级都随之丢失。

## 做法

1. 列出页面每个区块的数据来源与源端更新条件（只在 Success 时更新、失败分支是否保留旧值）；目标按区块分别保存结果与错误，不用 a === null || b === null 一类条件决定整页错误。
2. 源端先用缓存或首页数据填充再请求详情时，网关先取缓存构造基础数据，详情失败时返回带缓存的结果并轻提示；无缓存时的显示按源端首载失败与空值分支实现，缺值占位取源端该字段的占位文案或资源。
3. XML 里已有的静态文案与图标作为首帧默认值同步渲染；共享快照的加载钩子只合并本来源负责的字段，不新建快照整体替换。
4. 源端失败分支保留旧数据、只在成功时替换时：整页错误或重试态只绑定主列表加载失败且没有可用数据；次级动作（权限拒绝、不支持、解析失败）用 Toast、提示条或对话框呈现；catch 不清空已成功的列表，刷新失败时保留已有内容并给提示与重试入口，刷新用局部指示，不用盖住其他分区的全屏遮罩。

## 可选检查

- 逐个模拟 ViewModel 的每个错误值，确认只有主列表加载失败且无可用数据时才显示整页错误

来源支持：5 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-4dad731ff5682f738fa4](../../../store/cases/case-4dad731ff5682f738fa4/6168f9d70770bc1fc216ded48fcf43b43c7ca6922885699c785f7542476f9da0.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`6168f9d70770bc1fc216ded48fcf43b43c7ca6922885699c785f7542476f9da0`
- [case-afea6fdc0d6edca2222e](../../../store/cases/case-afea6fdc0d6edca2222e/943782f7696306d4b8a9d5148b45d71ab364280f97477d24b7a2b0388027b0b3.json) · 结论：recommendation:5
  卡片版本：`943782f7696306d4b8a9d5148b45d71ab364280f97477d24b7a2b0388027b0b3`
- [case-cf6e5b0120e30d1395dd](../../../store/cases/case-cf6e5b0120e30d1395dd/b9d68df544a7243c08d693c40c5cc2e10739c6b1ade0979e0a38df5aaf8e78e4.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`b9d68df544a7243c08d693c40c5cc2e10739c6b1ade0979e0a38df5aaf8e78e4`
- [case-dc0bf21d0784e98b919e](../../../store/cases/case-dc0bf21d0784e98b919e/788129a45070f5a873255b341d99c5563cffe8138e365f20cedc69e3f7ed4ab8.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`788129a45070f5a873255b341d99c5563cffe8138e365f20cedc69e3f7ed4ab8`
- [case-e7af91622703010ed47f](../../../store/cases/case-e7af91622703010ed47f/ca3bef0c958a548e08983f174d26cced13cdd7ea2a57be3536b0c7ea8d2a7c32.json) · 结论：diagnosis, recommendation:1
  卡片版本：`ca3bef0c958a548e08983f174d26cced13cdd7ea2a57be3536b0c7ea8d2a7c32`

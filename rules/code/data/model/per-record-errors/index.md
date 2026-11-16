# 逐条解析和导入时单条记录出错的处理

agent 会看到什么：源端在循环里逐条 getJSONObject、解析、insert，或列表解析里单条记录的字段取不到；产物里先全量校验再写库、单条失败就 throw 让整页失败

## 规矩

- rule-46836db0df01｜源端恢复在循环里逐条解析插入时，目标逐条插入、遇错即停、已插入保留｜读到：源码恢复流程在 for 循环里逐条 getJSONObject → 解析 → insert → getJSONArray(子项) → insertAll；写错：目标先全量解析校验再写库；子项为 null 或缺键时读成空数组 `[]` 继续
- rule-efd1d0e922ce｜列表解析里单条记录的展示文本为空时降级为空串，catch 记下具体异常，不让整页失败｜写错：解析器里单条记录的展示字段校验失败就 throw，外层 catch 把整页置为加载失败态，只显示通用错误文案，没记下 error.message

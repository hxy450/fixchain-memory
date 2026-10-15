# 源端显示值经带兜底的访问器或码值映射函数取得时，目标调用已移植的同一函数，不改读原始字段、不透传 code、不自拟兜底

ID：`lesson-1fa08bf929cfced0ff34` · 版本：4

[本主题](index.md)

## 何时使用

功能接线阶段，把源端刷新函数里的显示赋值（如 text = Manager.getX()、text = Util.codeToText(code)）翻译成目标组件状态，或把登录判定与显示字段映射成文案表达式时

## 适用情境

源端在某一分支调用带空值兜底的访问器（例：已登录但昵称为空时返回“用户{id}”或默认昵称），另一分支才显示“未登录”等占位文案；或经工具类把数值码映射为显示文案（天气码、等级、方向等）。目标侧会话或仓库层保留原始字段，可能已移植同名兜底方法或映射函数，组件状态是普通字段，工程里有现成的占位字符串资源。

## 例外与边界

- 整条记录映射成多字段 UI 模型（图标与颜色成对下传、构建器回退）：按适配层逐字段赋值的经验处理

## 原因

访问器或映射函数的方法体才是显示语义（空值兜底、分支分流、码值到文案的对照表）；改读原始字段或 toString() 后，接线者会用手边的占位文案补空值，把另一分支的文案挪进本分支，或直接显示原始码。把显示字段判空并入登录判定，还会让有效会话显示成未登录。

## 做法

1. 源端调用的是访问器或映射函数而非字段时，目标同一分支调用已移植的等价函数（没有就先移植）；占位文案只放在源端对应的分支。
2. 先读访问器方法体的空值兜底，再按分支组合（例：已登录 + 显示字段为空）逐分支核对目标表达式的结果与源端一致；登录判定（token/session）与显示回退链分开实现，新增的字段判空不能改变登录/未登录分支的判定依据。
3. 不要把未登录占位资源复用为已登录用户的空值兜底；为“已登录、显示字段为空、id 存在”写一条显示用例，期望值取源端回退结果。
4. 访问器返回 ResourceStr 而状态是 string 时，按工程已有方式解析资源（宿主 context 判空同时排除 undefined 与 null），不因类型不合回退成占位字符串。
5. 源端经工具类把数值码映射成文案时，目标调用同表的映射函数，不用 toString() 输出原始码；再按 UI 数据模型逐字段核对每个显示字段都有来源。

来源支持：3 张卡 · 3 次迁移 · 3 个应用

## 来源（按需复核）

- [case-1cfad6c2eaf32070939a](../../../store/cases/case-1cfad6c2eaf32070939a/22c647b810d09efec62c8bd0f841bcc9e4f190e1a6f8e9f9a5ac20ff7e81d33d.json) · 结论：recommendation:3
  卡片版本：`22c647b810d09efec62c8bd0f841bcc9e4f190e1a6f8e9f9a5ac20ff7e81d33d`
- [case-1ea05be22c68b8603ea7](../../../store/cases/case-1ea05be22c68b8603ea7/4cc7a73bb9841e4befe283207b510fec7f3ef0deb69ddb7ca78c89528097c31c.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`4cc7a73bb9841e4befe283207b510fec7f3ef0deb69ddb7ca78c89528097c31c`
- [case-ca0f19f5d338e37a710e](../../../store/cases/case-ca0f19f5d338e37a710e/29933bfec96bf8cbcf277775edf599de86352a66da73c5531c5cd994d5ced700.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`29933bfec96bf8cbcf277775edf599de86352a66da73c5531c5cd994d5ced700`

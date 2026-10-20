# onPreferenceChange 返回 true 即接受并持久化新值：其中发起的验证按源顺序先落值再补偿，取消不回滚

ID：`lesson-8b84279c4ecbeaf26e3e` · 版本：1

[本主题](index.md)

## 何时使用

设置页实现阶段，把 Preference 的 onPreferenceChange 监听（含其中发起的验密、确认弹窗）翻译成目标开关回调时；规格提取阶段描述这类联动流程时

## 适用情境

源端在 onPreferenceChange 里发起异步验证后立即 return true，验证成功的回调只做补偿动作（如再次 setChecked 同值），取消没有回滚分支；目标用受控 Toggle 与回调实现，写者倾向“先回滚、验证成功才落值”。

## 原因

onPreferenceChange 的返回值决定这次变更是否被接受：返回 true 时 Preference 随即持久化新值并更新显示，之后到达的验证结果只能做补偿。改成“先回滚、成功才落值”会颠倒落值时刻与失败分支，取消时多出回滚，开关显示与偏好值都和源端不同。

## 做法

1. 按返回值迁移：源端 return true 时先写入新值并更新开关，再发起验证，验证回调只执行源端写明的补偿，取消或失败不回滚；源端 return false 时才保持旧值，由回调决定是否写入。
2. 源设置页只在 onResume 等时机重读的状态，目标不额外订阅事件即时刷新。
3. 规格写这类联动流程时逐步写出落值时刻（立即生效或事后补偿）与失败分支。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-a293ed8cf3fa860f8330](../../../store/cases/case-a293ed8cf3fa860f8330/5b59203d875d7187e99f77129cb00b802dad0c45e4571c82b666606995535ad5.json) · 结论：diagnosis, recommendation:5, recommendation:6
  卡片版本：`5b59203d875d7187e99f77129cb00b802dad0c45e4571c82b666606995535ad5`

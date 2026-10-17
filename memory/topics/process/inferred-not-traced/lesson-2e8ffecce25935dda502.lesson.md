# 源端并存新旧两套实现时，以当前构建启用或目标页对应的实现为行为基准

ID：`lesson-2e8ffecce25935dda502` · 版本：2 · 阶段：spec/execute · 主题：[process/inferred-not-traced](index.md)

概要：新旧两套实现并存时以当前构建启用的为基准

信号：`buildConfigField`, `manifestPlaceholders`, `gradle`

## 何时使用

规格提取与实现阶段，同一能力在源码中有新旧两套实现（构建开关二选一，或新旧页面并存），需要确定行为断言与时序规则时

## 适用情境

源码以 buildConfigField、manifestPlaceholders 等开关在两套实现间择一，或旧版与新版页面并存且各有生命周期与竞态规则；两者在若干路径上行为不同，目标只建一套。

## 原因

把两套行为取并集，或把旧页规则写成通用规则，会让目标实现停用实现的语义（如换集时收尾上一项、跳过即标记），或给新页套上不属于它的状态门。

## 做法

1. 先在 gradle 构建脚本查出开关在当前构建的取值，以启用的实现为基准；停用实现只作对照。
2. 冲突路径逐条标明来源实现；要偏离启用实现时登记决策，不默认取并集。
3. 竞态与生命周期规则标明适用页面，目标页以对应的源页面为准。
4. 交叉验证时把参考文档中已记录的构建事实与规格中“二选一/取并集”的表述对照。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [组合异源切换步骤时不先改写入口守卫读取的状态](../../app/playback/lesson-6b2879705254045a49c5.lesson.md)（共享 1 张卡）
- [surface 按对应源页绑定，画面等比内接](../../app/playback/lesson-6b4950ca1655ae7bcb8f.lesson.md)（共享 1 张卡）
- [Stack 子项 .align() 无效，对齐用满高容器](../../ui/layout/constraints/lesson-92aee54a305ea0bde363.lesson.md)（共享 1 张卡）
- [manifest 未声明的窗口缺省解析成目标值并指派](../../app/entry/lesson-c1d7ec16bb02aa152c33.lesson.md)（共享 1 张卡）

来源支持：2 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-37177617eaf19edf532c](../../../../store/cases/case-37177617eaf19edf532c/ae8827db4c016f93d4e80a6d6e7efdc36258af5fe1c6e1c8c8a2eedf85141cf5.json) · 结论：diagnosis, rec-d0b0a8e134, rec-9ce2394088, rec-1001150e3e
  卡片版本：`ae8827db4c016f93d4e80a6d6e7efdc36258af5fe1c6e1c8c8a2eedf85141cf5`
- [case-5e35bb283520acf3bd35](../../../../store/cases/case-5e35bb283520acf3bd35/954c420a6eb53234d9a40e9851863e13e6a2b9e3e2195abc6f71fcfe048dcf4f.json) · 结论：rec-e1fd2b65e7
  卡片版本：`954c420a6eb53234d9a40e9851863e13e6a2b9e3e2195abc6f71fcfe048dcf4f`

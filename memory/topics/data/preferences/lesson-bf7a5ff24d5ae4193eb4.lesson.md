# 迁移 SharedPreferences 读写契约时按源端全部读写点定值格式、缺键与空串的区分，以及 put 被注释的项是否真的持久化

ID：`lesson-bf7a5ff24d5ae4193eb4` · 版本：1 · 阶段：spec/execute · 主题：[data/preferences](index.md)

概要：偏好契约按源全部读写点定格式、缺键与持久性

信号：`SharedPreferences`, `getString`, `putString`, `editor.putString`, `hasSync`, `getSync`, `putSync`

## 何时使用

规格提取与偏好封装、设置读写实现阶段，确定偏好键清单、值格式与缺键判定时

## 适用情境

源端同一偏好由设置页、弹层、会话代码等多处读写，值是带分隔符的拼接串；有的读取用 getString(key, null) 以 null 判缺键，空串本身是合法值；有的设置项旁边的 editor.putString 被注释掉，只调用会话对象的 setter。目标偏好封装只有 get(key, def)/put，没有存在性查询，读写方由不同任务分别编写。

## 原因

写者自拟格式时，设置页写入的值在会话侧解析失败并回落默认值，用户的选择不生效；以 '' 作缺键哨兵，会把合法的空串当缺键丢掉；把只改会话的设置当成持久键，就新建了源端没有的键，会话侧的值却不随设置变化。三种偏差都能编译运行，只在实际切换后才表现出来。

## 做法

1. 实现偏好读写前读源端该键的全部读写函数，格式（分隔符、顺序、单位）照源函数；同工程已有写者时以它为准，读写双方同口径。
2. 源端以 getString(key, null) 区分缺键、空串又合法时，偏好封装补存在性查询（如 Preferences.hasSync），不用 '' 作缺省哨兵；封装归其他任务时登记契约缺口，不在注释里接受数据丢失。
3. 规格列“读写偏好键”清单时按源码实际执行的写路径判定：put 被注释、只调会话 setter 的项登记为会话态 setter 及其消费方，不列为持久键。

## 可选检查

- 对格式有疑问时，用设置页写入的值调用会话侧读取，应解析回同一值。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [下“不存在”结论前确认检索覆盖完整声明与范围](../../process/unverified-as-fact/lesson-8b7a50eeb92fc3bdb1e7.lesson.md)（共享 2 张卡）
- [功能对齐以代码落点为准，空回调不算实现](../../process/claimed-without-receipt/lesson-9147be4d87153de9c5b6.lesson.md)（共享 2 张卡）
- [必读 skill 与源码逐份读全，截断即重读再写码](../../process/unloaded-input/lesson-42df1ac4d4030421da34.lesson.md)（共享 1 张卡）
- [跨文件补实现的功能登记带负责方与验证的移交项](../../process/handoff-loss/lesson-4f81eeea17b94190c2de.lesson.md)（共享 1 张卡）
- [规格与源码冲突按源实现，例外只认决策 ID](../../process/secondary-over-source/lesson-7a065e8fe384b8c462cc.lesson.md)（共享 1 张卡）

来源支持：3 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-91084f18203ecc5e7036](../../../../store/cases/case-91084f18203ecc5e7036/b2ef3d93c321f92d42c3adeb2614a39fc4a1d58051f93808ce0ad907fbc2e561.json) · 结论：diagnosis, rec-c134f060ba
  卡片版本：`b2ef3d93c321f92d42c3adeb2614a39fc4a1d58051f93808ce0ad907fbc2e561`
- [case-bebaba79e02c02cca6a1](../../../../store/cases/case-bebaba79e02c02cca6a1/0bb08dc9692fa796ed9358ccd25cab4cce38bbf4405d43ef5d294e5f5d0cd0a6.json) · 结论：diagnosis, rec-3eb136c00f
  卡片版本：`0bb08dc9692fa796ed9358ccd25cab4cce38bbf4405d43ef5d294e5f5d0cd0a6`
- [case-d5698429a34c85664785](../../../../store/cases/case-d5698429a34c85664785/7ab31e28c5c952c7e5c7b20548bde4e7bd5dbfb464237ece26dfb1b81c2cebe0.json) · 结论：diagnosis, rec-4c947bd9b1
  卡片版本：`7ab31e28c5c952c7e5c7b20548bde4e7bd5dbfb464237ece26dfb1b81c2cebe0`

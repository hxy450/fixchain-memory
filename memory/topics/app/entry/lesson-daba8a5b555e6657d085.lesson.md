# intent-filter 逐条映射 module.json5 skills：分享类登记 sendData，多文件用 maxFileSupported

ID：`lesson-daba8a5b555e6657d085` · 版本：6 · 阶段：spec/execute · 主题：[app/entry](index.md)

概要：intent-filter 逐条映射为 skills

信号：`intent-filter`, `ohos.want.action.sendData`, `maxFileSupported`, `SEND_MULTIPLE`, `ohos.want.action.sendMultipleData`, `ohos.want.action.search`, `PROCESS_TEXT`, `EXTRA_STREAM`, `wantConstant.Params`, `SHARE_ABSTRACT_KEY`, `systemShare.getSharedData`

## 何时使用

规格提取与入口配置阶段，把入口 Activity 的 intent-filter 映射为 module.json5 skills，并为外部 Want 的载荷确定解析键时

## 适用情境

源入口 Activity 有多条非深链 intent-filter（SEARCH、SEND、SEND_MULTIPLE、PROCESS_TEXT、AUTO_SEND 等），源码按 Intent.EXTRA_SUBJECT、EXTRA_TEXT、EXTRA_STREAM 读载荷；技能参考可能声称调用某系统能力（如 cameraPicker）须声明对应的 skill。

## 原因

skills 是本应用受理外部 Want 的过滤器：合并或漏登记的 action 让系统分享面板、搜索等入口找不到本应用，多出的 skill 让应用成为该类请求（如系统相机）的候选；自造的载荷键与系统和发送方实际传入的键对不上，入口收到 Want 也取不到内容。

## 做法

1. 逐条列出 intent-filter 并各给一条 skills 映射（actions、entities、uris 的 scheme 或 type/utd）；作为系统分享目标时 SEND 与 SEND_MULTIPLE 都落到 ohos.want.action.sendData，多文件以 uris 中 maxFileSupported 大于 1 表达（Share Kit 接收方只登记 sendData；HarmonyOS 文档 share-interface-description，访问于 2026-10-17），ohos.want.action.sendMultipleData 只见于 API 9 起废弃的 @ohos.ability.wantConstant，仅在需兼容显式指定该 action 的发送方时额外登记；其余平台有对应 action 的分别登记（SEARCH → ohos.want.action.search，常量同样只见于废弃的 @ohos.ability.wantConstant，Stage 文档未说明系统搜索派发该 action；本机 SDK API 24 @ohos.ability.wantConstant.d.ts），不并入他条，也不改由应用内组件代替。
2. 分享目标按 Share Kit 要求在 uris 中写 utd 与 maxFileSupported（maxFileSupported 默认 0，即不支持该类文件；scheme 为预留字段，写 file 也不起过滤作用；HarmonyOS 文档 share-interface-description，访问于 2026-10-17），缺这些时系统分享面板不列出本应用。
3. 源 manifest 没有对应 intent-filter 的 skill 不加；参考资料称“调用某系统能力须声明某 skill”时，先在 SDK d.ts 或官方文档核实，调用 picker 等系统能力不需要受理型 skill。
4. 载荷键不自造：并列读取 Android 原键（android.intent.extra.SUBJECT、TEXT、STREAM）、系统标准键（wantConstant.Params 的 CONTENT_TITLE_KEY、SHARE_ABSTRACT_KEY）与 systemShare.getSharedData；查不到来源的键在规格中标为未知，不写成契约。
5. 源端分发入口 Intent 有前置门（如密码验证通过后才处理）时，快存、分享落库等动作保持在该门之后，不放进 Ability 冷启动的分发里直接执行。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [深链声明 skills、domainVerify，隐式验收](lesson-d77baa7494930d485425.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-7b71b27d8bbbbbd73267](../../../../store/cases/case-7b71b27d8bbbbbd73267/eae79498ed3c968868f59d3c0d5142443209228899494c6d32604f7e84767fc3.json) · 结论：diagnosis, rec-877999520f, rec-03fea4fa4b, rec-e6e574330b, rec-5cc524d6f6
  卡片版本：`eae79498ed3c968868f59d3c0d5142443209228899494c6d32604f7e84767fc3`

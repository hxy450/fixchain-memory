# intent-filter 逐条映射为 module.json5 skills：有对应 action 的不合并，载荷键不自造，源端没有的不加

ID：`lesson-a23ad0b53c75e49ca117` · 版本：1

[本主题](index.md)

## 何时使用

规格提取阶段把 AndroidManifest 的 intent-filter 与入口 Intent 载荷翻成 module.json5 skills 与 Want 参数契约时；接线阶段按笔记或 skill 参考给出的片段修改 skills 时

## 适用情境

源 Activity 声明多条 intent-filter（SEARCH、VIEW 自定义 scheme、SEND/SEND_MULTIPLE */*、PROCESS_TEXT 等），入口分发读取 Intent.EXTRA_* 键，并可能在初始化或验密门之后才处理 Intent；目标为 UIAbility 的 module.json5 skills（actions、entities、uris，分享目标需 utd 与 maxFileSupported）与 Want parameters、systemShare 载荷；skill 参考或交接笔记可能给出“调用某系统能力须声明某 skill”的片段。

## 原因

skills 是本应用受理外部 Want 的过滤器：合并或漏登的 intent-filter，其入口不会被系统匹配（分享面板不出现本应用、搜索与多文件分享收不到）；多加的 skill 会让应用成为无关能力（如系统相机）的候选。自造的载荷键与外部调用方实际写入的键对不上，入口能拉起却读不到内容。

## 做法

1. 逐条列出 intent-filter，每条给一项 skill：action 映射到平台对应的 ohos.want.action.*（如 SEARCH → search，SEND → sendData，SEND_MULTIPLE → sendMultipleData，VIEW → viewData），data 映射为 uris（scheme/host/path，分享目标写 utd 与 maxFileSupported）；有对应 action 的不并入他条，也不改由应用内组件承接。
2. 载荷契约并列写出两侧：源端读取的 Intent.EXTRA_* 字符串值（如 android.intent.extra.SUBJECT）与目标标准键或接口（wantConstant.Params.CONTENT_TITLE_KEY、SHARE_ABSTRACT_KEY，系统分享用 systemShare.getSharedData）；查不到出处的键写为未知并说明影响，不写成契约。
3. 只为源 manifest 里有对应 intent-filter 的入口写 skill；参考文档或笔记要求“调用某系统能力须声明某 entity/action”（如拉起系统相机）时，先用 SDK d.ts 或官方文档复核，调用系统能力不需要本应用声明受理同类 Want。
4. 入口分发照抄源端前置条件：源端在初始化或验密门受理之后才处理 Intent 的，目标把落库、分享保存等动作放在同一道门之后，不在 EntryAbility 冷启分发里直接执行。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-7b71b27d8bbbbbd73267](../../../store/cases/case-7b71b27d8bbbbbd73267/eae79498ed3c968868f59d3c0d5142443209228899494c6d32604f7e84767fc3.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:4, recommendation:5
  卡片版本：`eae79498ed3c968868f59d3c0d5142443209228899494c6d32604f7e84767fc3`

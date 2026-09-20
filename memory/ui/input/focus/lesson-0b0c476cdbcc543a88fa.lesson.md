# 翻译「离开组合即销毁」的 remember 状态时，逐项列出目标框架会替用户恢复的 UI 状态（焦点、IME 等）

ID：`lesson-0b0c476cdbcc543a88fa` · 版本：1

[本主题](index.md)

## 何时使用

规格提取阶段，把源端 remember（非 rememberSaveable）随组合销毁的状态语义翻译成目标端复位方案时

## 适用情境

源页面靠 remember 在离开组合时丢弃全部状态，其中 focused 等由框架事件驱动的字段直接决定显示分支；目标端该页面常驻在 Navigation 的 NavBar（Stack/Tabs 保活）中，经 pushPath 进入子页后再系统返回。

## 原因

F005 spec 的 AC67 要求本身正确（返回后 focused=false），但复位机制只给 resetState=new SearchState，并把 TextInput.onFocus/onBlur 无条件映射到 focused；平台差异分析只覆盖 Tabs/NavDestination 保活，漏掉 ArkUI Navigation 在 NavDestination pop 后把窗口焦点交还 NavBar 上次获焦节点——生成期全部材料零处提及该行为，属平台知识材料缺口。

## 做法

1. 除数据字段外逐项列出目标框架会替用户恢复的 UI 状态（焦点、IME、滚动位置、选区），对每项写明 ArkUI 侧的复位或判别手段。
2. 由框架事件驱动的业务字段（如 focused）把「返回后为 false」写成可机械核对的验收步骤（push→Back 往返后 dump TextInput.focused），不只留 判:ui。

## 检查

- 一次 push→系统返回后的 dump：TextInput focused=false、无键盘；spec 里每个框架恢复项都有对应复位手段。

## 来源（按需复核）

经验是有适用范围的历史建议。核查来源时同时看结论与 unknown；来源卡未随阅读包复制。

- [case-c6aa20bd8974dabefc7b](../../../../store/cases/case-c6aa20bd8974dabefc7b/9d7bebdf60e8f37ea22ecebf4a50628741a64bae1510b36814dbd2008f49b057.json) · 结论：diagnosis, recommendation:1
  卡片版本：`9d7bebdf60e8f37ea22ecebf4a50628741a64bae1510b36814dbd2008f49b057`

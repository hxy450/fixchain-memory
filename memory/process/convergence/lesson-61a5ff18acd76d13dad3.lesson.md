# 收敛 worker 的派工清单逐条列出 mapping 中的全部共享原语，worker 逐项对账后再整文件重写

ID：`lesson-61a5ff18acd76d13dad3` · 版本：1

[本主题](index.md)

## 何时使用

收敛阶段，派发 W2 类 worker 把页面私有实现替换为共享基座原语（阴影/排版/颜色映射函数）并允许其整文件重写时

## 适用情境

mapping 文档已有共享原语节（如 §5 shadowFor），页面内联写法与之不一致；派工清单只点名部分对接点。

## 原因

G1 W2b 已读到 §5「e=3 自绘 Categories 卡」与 shadowFor 导出，整文件重写仍保留 OUTER_DEFAULT_XS，因为派工清单未点名 §5；Snackbar 不在 F002 对接点清单，字面 shadow 一直保留到修复期。

## 做法

1. 派工清单逐条列出 mapping 中的全部共享原语与其对接点；worker 收到后对读到的 mapping 节逐项对账，替换完成前不整文件重写。

## 检查

- 全工程 grep 每个共享原语对应的原生属性（如 `.shadow(`），出现处均为共享函数调用。

## 来源（按需复核）

经验是有适用范围的历史建议。核查来源时同时看结论与 unknown；来源卡未随阅读包复制。

- [case-75329cae60986f74dc43](../../../store/cases/case-75329cae60986f74dc43/e05464cbccdf6181891a9fd2ddf2bbc2143a88e5f4fc4dcc3b1be803917b20cf.json) · 结论：recommendation:3
  卡片版本：`e05464cbccdf6181891a9fd2ddf2bbc2143a88e5f4fc4dcc3b1be803917b20cf`

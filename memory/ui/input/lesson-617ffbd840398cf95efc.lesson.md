# 源端受控输入框的长度上限用 TextInput.maxLength 实现，不靠 onChange 里拒绝写回

ID：`lesson-617ffbd840398cf95efc` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段，把源端输入框的长度上限等输入约束翻译成 ArkUI TextInput 属性与事件时

## 适用情境

源端 Compose TextField/OutlinedTextField 以 value = 状态受控，在 onValueChange 中按条件决定是否写回（如 if (it.length <= N) name = it）；目标端用 TextInput({ text: this.x }) 加 onChange 实现同一个输入框。

## 原因

Compose 输入框只显示状态值，拒绝写回就等于拒绝输入；ArkUI TextInput 以 text 单向初始化后自己维护编辑内容，onChange 中不写回只让状态停住，输入框仍可显示超出的字符。来源两处生成者都读到了源码条件，把它原样搬进 onChange；生成期参考只给出 EditText → TextInput 与“onChange 写回加校验”的示例，没有受控语义或 maxLength 的对照。修复加 .maxLength(N) 后设备实测追加字符被拒；修复前没有做设备复现。

## 做法

1. 长度上限写成 .maxLength(N)，N 取源码条件中的值；onChange 只负责同步状态。字符集类限制可用 inputFilter。
2. 逐条列出源码 onValueChange 中的拒绝条件，确认每条在 ArkUI 侧都有能阻止输入显示的属性，而不只是让状态不更新。

## 可选检查

- 能上设备时输入 N+1 个字符，核对 TextInput 文本长度。

## 来源（按需复核）

- [case-e3cd92963aa40d922fdc](../../../store/cases/case-e3cd92963aa40d922fdc/9788f0e9846113141c74603b6f4b949ae84f08bb07d5f725949650546de97620.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`9788f0e9846113141c74603b6f4b949ae84f08bb07d5f725949650546de97620`

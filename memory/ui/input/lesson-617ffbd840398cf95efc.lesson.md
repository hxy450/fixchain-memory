# 源端受控输入框在 onValueChange 拒绝写回时，用 onWillChange 返回 false 或 maxLength 阻止显示

ID：`lesson-617ffbd840398cf95efc` · 版本：4

[本主题](index.md)

## 何时使用

界面实现阶段，把源端输入框的长度上限等输入约束翻译成 ArkUI TextInput 属性与事件时

## 适用情境

源端 Compose TextField/OutlinedTextField 以 value = 状态受控，在 onValueChange 中按条件决定是否写回（如 if (it.length <= N) name = it，或数值格式不合法时直接 return、不回调上层）；目标端用 TextInput({ text: this.x }) 加 onChange 实现同一个输入框，可能由父组件持有值并以“父值不变即回退”设计公共输入组件。

## 例外与边界

- 源端的约束来自 EditText 的 digits、InputFilter 或 maxLength 等非受控过滤：按这些过滤器的语义映射

## 原因

Compose 输入框只显示状态值，拒绝写回就等于拒绝整次输入；ArkUI TextInput 以 text 单向初始化后自己维护编辑内容，onChange 中不写回只让状态停住，输入框仍显示被拒的字符。

## 做法

1. 逐条列出源码 onValueChange 中的拒绝条件。长度上限（如 if (it.length <= N) 才写回）：.maxLength(N) 能阻止逐字输入超过 N；源端对一次超长输入（如粘贴）是整次拒绝，而 maxLength 遇超长粘贴是截断还是拒绝，text_input.d.ts 没有说明，要保持整次拒绝时，在 onWillChange（text_input.d.ts，API 15 起）里用与源码相同的判断返回 false。长度按源端 length 的计数单位（UTF-16 码元）比较。
2. 长度之外的拒绝条件（如数值格式不合法时直接 return）在 onWillChange 中返回 false，框内保持宿主值；不靠父组件“不更新值”回退。字符集类限制可用 inputFilter，onChange 只负责同步状态。
3. 确认每条拒绝条件在 ArkUI 侧都有能阻止输入显示的属性或回调，而不只是让状态不更新；目标 API 低于 15 时把无法整次拒绝的条件写进差异登记。

## 可选检查

- 能上设备时输入 N+1 个字符，核对 TextInput 文本长度；只用 maxLength 时再粘贴一段超过 N 的文本，核对是否与源端整次拒绝一致；格式类条件再输入一个非法字符（如字母或第二个小数点），核对框内文本不变。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-e332c2cc4929f36c08c7](../../../store/cases/case-e332c2cc4929f36c08c7/99990fa89f7be35793b896d170fd65a4dbe46e7c285f99e1fd707e9d8d36f301.json) · 结论：diagnosis, recommendation:5
  卡片版本：`99990fa89f7be35793b896d170fd65a4dbe46e7c285f99e1fd707e9d8d36f301`
- [case-e3cd92963aa40d922fdc](../../../store/cases/case-e3cd92963aa40d922fdc/9788f0e9846113141c74603b6f4b949ae84f08bb07d5f725949650546de97620.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`9788f0e9846113141c74603b6f4b949ae84f08bb07d5f725949650546de97620`

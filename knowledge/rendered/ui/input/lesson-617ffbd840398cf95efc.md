# 源端受控输入框的拒绝条件要阻止文本显示：长度上限用 TextInput.maxLength，其他拒绝条件在 onWillChange 返回 false，不靠 onChange 里不写回

## 何时使用

界面实现阶段，把源端输入框的长度上限等输入约束翻译成 ArkUI TextInput 属性与事件时

## 适用情境

源端 Compose TextField/OutlinedTextField 以 value = 状态受控，在 onValueChange 中按条件决定是否写回（如 if (it.length <= N) name = it，或数值格式不合法时直接 return、不回调上层）；目标端用 TextInput({ text: this.x }) 加 onChange 实现同一个输入框，可能由父组件持有值并以“父值不变即回退”设计公共输入组件。

## 原因

Compose 输入框只显示状态值，拒绝写回就等于拒绝输入；ArkUI TextInput 以 text 单向初始化后自己维护编辑内容，onChange 中不写回只让状态停住，输入框仍可显示超出的字符。来源两处生成者都读到了源码条件，把它原样搬进 onChange；生成期参考只给出 EditText → TextInput 与“onChange 写回加校验”的示例，没有受控语义或 maxLength 的对照。修复加 .maxLength(N) 后设备实测追加字符被拒；修复前没有做设备复现。

## 做法

1. 长度上限写成 .maxLength(N)，N 取源码条件中的值；onChange 只负责同步状态；源端 onValueChange 里除了按条件写回还有别的动作（如清掉错误提示、触发查询）时，这些动作照样留在 onChange 里，不随拒绝条件一起移走。字符集类限制可用 inputFilter。
2. 长度与字符集之外的拒绝条件（数值格式、第二个小数点、取值范围等），在 onWillChange（API 15 起提供）中用与源码相同的判断返回 false 拒绝本次变更，框内保持宿主值；不靠父组件“不更新值”回退。
3. 逐条列出源码 onValueChange 中的拒绝条件，确认每条在 ArkUI 侧都有能阻止输入显示的属性或回调，而不只是让状态不更新。

## 可选检查

- 能上设备时输入 N+1 个字符，核对 TextInput 文本长度；格式类条件再输入一个非法字符（如字母或第二个小数点），核对框内文本不变。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因〕父组件持有的值不变（onChange 里不写回）时，TextInput 不会回显旧值，被拒的字符仍留在输入框里
- 〔做法第 1 步〕TextInput.maxLength 取值 [0, 2^31-1]，不设或设异常值时不限长度，设小数时取整数部分
- 〔做法第 1 步〕TextInput 设了 .maxLength(N) 后，在设备上输入到 N 个字符再追加，框内文本仍是 N 个字符
- 〔做法第 1 步〕TextInput.inputFilter 按正则过滤输入：匹配的才显示；单字符输入时只按单个字符匹配，粘贴等多字符输入按整串匹配；API 11 起设了 inputFilter 且输入不为空时，type 自带的文本过滤失效
- 〔做法第 2 步〕TextInput.onWillChange（API 15 起）在文本变更前触发：返回 false 拦截这次变化，框内文本不变；返回 true 放行，随后触发 onChange

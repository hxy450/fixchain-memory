# 源端受控输入框的拒绝条件要阻止文本显示：长度上限用 TextInput.maxLength，其他拒绝条件在 onWillChange 返回 false，不靠 onChange 里不写回

ID：`lesson-617ffbd840398cf95efc` · 版本：3 · 阶段：execute · 主题：[ui/interaction/input](index.md)

概要：拒绝输入用 maxLength 或 onWillChange

信号：`maxLength`, `onValueChange`, `onChange`, `onWillChange`, `inputFilter`, `OutlinedTextField`, `TextField`, `TextInput`

## 何时使用

界面实现阶段，把源端输入框的长度上限等输入约束翻译成 ArkUI TextInput 属性与事件时

## 适用情境

源端 Compose TextField/OutlinedTextField 以 value = 状态受控，在 onValueChange 中按条件决定是否写回（如 if (it.length <= N) name = it，或数值格式不合法时直接 return、不回调上层）；目标端用 TextInput({ text: this.x }) 加 onChange 实现同一个输入框，可能由父组件持有值并以“父值不变即回退”设计公共输入组件。

## 原因

Compose 输入框只显示状态值，拒绝写回就等于拒绝输入；ArkUI TextInput 以 text 单向初始化后自己维护编辑内容，onChange 中不写回只让状态停住，输入框仍可显示超出的字符。来源两处生成者都读到了源码条件，把它原样搬进 onChange；生成期参考只给出 EditText → TextInput 与“onChange 写回加校验”的示例，没有受控语义或 maxLength 的对照。修复加 .maxLength(N) 后设备实测追加字符被拒；修复前没有做设备复现。

## 做法

1. 长度上限写成 .maxLength(N)，N 取源码条件中的值；onChange 只负责同步状态。字符集类限制可用 inputFilter。
2. 长度与字符集之外的拒绝条件（数值格式、第二个小数点、取值范围等），在 onWillChange 中用与源码相同的判断返回 false 拒绝本次变更，框内保持宿主值；不靠父组件“不更新值”回退。
3. 逐条列出源码 onValueChange 中的拒绝条件，确认每条在 ArkUI 侧都有能阻止输入显示的属性或回调，而不只是让状态不更新。

## 可选检查

- 能上设备时输入 N+1 个字符，核对 TextInput 文本长度；格式类条件再输入一个非法字符（如字母或第二个小数点），核对框内文本不变。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [Float 运算比较按 float32 后用 ===](../../../arkts/runtime-semantics/lesson-0deb51172ebdd2e056a9.lesson.md)（共享 1 张卡）
- [短提示音保留混播与播放中 start 不重启语义](../../../app/playback/lesson-5475edc47af05c1c6a5b.lesson.md)（共享 1 张卡）
- [长按手势显式补系统长按触感](../gestures/lesson-8a752faf9f5dff52e3ff.lesson.md)（共享 1 张卡）
- [Slider steps 翻步长：区间/(steps+1)](../selectors/lesson-d715fa78ada2e79a5fd2.lesson.md)（共享 1 张卡）
- [底部面板按实际高度定档，显式关 showClose](../../dialog/frame/lesson-df1f691759f84ba9e688.lesson.md)（共享 1 张卡）

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-e332c2cc4929f36c08c7](../../../../../store/cases/case-e332c2cc4929f36c08c7/99990fa89f7be35793b896d170fd65a4dbe46e7c285f99e1fd707e9d8d36f301.json) · 结论：diagnosis, rec-dfd7766071
  卡片版本：`99990fa89f7be35793b896d170fd65a4dbe46e7c285f99e1fd707e9d8d36f301`
- [case-e3cd92963aa40d922fdc](../../../../../store/cases/case-e3cd92963aa40d922fdc/9788f0e9846113141c74603b6f4b949ae84f08bb07d5f725949650546de97620.json) · 结论：diagnosis, rec-8cd3325bb4, rec-88f36fa9b6
  卡片版本：`9788f0e9846113141c74603b6f4b949ae84f08bb07d5f725949650546de97620`

# 源受控值是 TextFieldValue（文本加选区）时，回写文本后用 setTextSelection 落选区

审的是：代码
触发（任一种）：
- 读到：Compose 输入组件的受控值是 TextFieldValue，格式键算出新文本和新选区后以 TextFieldValue(新文本, 新选区) 交给 onValueChange；写错的样子：ArkTS 只回写了文本，新选区存在组件内的 @Local 变量里；TextAreaController 声明了却没有任何 setTextSelection 调用
适用范围：把 Compose 里文本和选区一体的受控输入（TextFieldValue）迁成 ArkUI TextArea 时
做法：
- TextArea({ text: …, controller: this.controller }) 把 controller 传进去；回写文本后调用 this.controller.setTextSelection(<新选区起点>, <新选区终点>)，起止取源端算出的 selection 的 start、end，只有光标时两个参数传同一个位置
- 交付前确认 controller 上确有 setTextSelection 调用，不只更新组件内状态
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- setTextSelection(selectionStart: number, selectionEnd: number, options?: SelectionOptions): void：TextAreaController 设置选区；起点从 0 算，小于 0 按 0、超过文本长度按文本长度处理，options 默认 MenuPolicy.DEFAULT（出处：鸿蒙 SDK 的 ets/component/text_area.d.ts，TextAreaController.setTextSelection）
- setTextSelection(selectionStart: number, selectionEnd: number, options?: SelectionOptions): void：同族接口：TextInputController 设置选区（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputController.setTextSelection）
- setTextSelection(selectionStart: number, selectionEnd: number, options?: SelectionOptions): void：同族接口：SearchController 设置选区（出处：鸿蒙 SDK 的 ets/component/search.d.ts，SearchController.setTextSelection）
未核实：卡里没写回写文本和 setTextSelection 的先后时序要不要隔一帧；卡里修好时的目标 SDK 是 6.1.1(24)，本机核实声明用的是 API 23
来源：1 张卡，1 个应用
- case-f63ccb39dd60e2abb04b（jerboa）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1

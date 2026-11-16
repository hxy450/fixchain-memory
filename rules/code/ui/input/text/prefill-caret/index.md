# setText 预填的输入框的光标位置

agent 会看到什么：读到源端（如 onCreateDialog 里）对 EditText 调 setText(...) 预填、光标在开头；产物里 TextInput({ text }) / TextArea({ text }) 有没有 controller 和首次 onFocus 时的 caretPosition(0)

## 规矩

- rule-aa698d8387a5｜源端 setText 预填的输入框，目标首次 onFocus 调 caretPosition(0)｜读到：源端 onCreateDialog 里对 EditText 调 setText(...) 预填；写错：目标 TextInput({ text }) / TextArea({ text }) 预填后没有 controller，也没有 caretPosition 处理，光标停在末尾

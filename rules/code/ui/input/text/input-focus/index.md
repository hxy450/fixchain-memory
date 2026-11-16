# 输入框的获焦和弹键盘

agent 会看到什么：源端 EditText 在首屏或 Dialog 弹出时获焦弹键盘；产物里 TextInput 的 defaultFocus / requestFocus、条件挂载的输入浮层和分段输入的节点

## 规矩

- rule-ad7c4a67b6dd｜首屏焦点应落在输入框时，首查完成后等窗口获焦再对 TextInput 请求焦点｜读到：规格验收写首屏输入框获焦并弹键盘；或源 manifest 未声明 windowSoftInputMode、布局里 EditText 前没有常驻可获焦视图；写错：目标页的 TextInput 没有任何初始焦点逻辑；或在 aboutToAppear、首查回调里直接 requestFocus，窗口还没激活，输入框 focused 却不弹键盘
- rule-608b06543a04｜条件挂载的页内浮层不靠 defaultFocus，输入框设 key、onAppear 里 requestFocus｜读到：源端每段输入是一个独立 Dialog（如 CustomDialog），弹出时里面的 EditText 获焦弹键盘；写错：目标用页内 Stack 里 if 条件挂载的浮层，TextInput 只写 .defaultFocus(true) 指望自动弹键盘，没有 key 和 requestFocus
- rule-97d3bbf3a0ea｜源端多段输入各是独立 Dialog 时，目标按段拆成独立分支节点，不用阶段标志复用同一 TextInput｜读到：两段流程各自建一个 Dialog（如 CustomDialog）、各自 inflate 布局并 findViewById 取自己的 EditText，第一段输满后 dismiss 再弹第二段；写错：目标只有一个受控 TextInput 节点，用阶段标志切换文案，并在 onChange 同一拍里清空输入值进入下一段
- rule-9b8ab5c5ff2a｜目标弹窗会把焦点自动给输入框时，加 defaultFocus 占位组件，不让弹窗一开就拉起键盘｜读到：源端弹窗里有 EditText，打开时不主动 requestFocus；写错：目标弹窗打开后焦点自动落到 TextInput 上，弹窗里没有 .defaultFocus(true) 的占位组件
- rule-d43167f57790｜弹层输入框只需获焦、不弹键盘时，设 enableKeyboardOnFocus(false)｜读到：源端对话框 EditText 只有 <requestFocus/>，没有 showSoftInput / setSoftInputMode；写错：目标 TextInput / TextArea 写了 .defaultFocus(true) 或由宿主 focusControl.requestFocus 获焦，但没写 .enableKeyboardOnFocus(false)
- rule-a9f6bcf5d99b｜宿主接通弹层内容组件时，逐条执行组件头注写给宿主的义务，如 then 里 requestFocus｜读到：弹层内容组件的头注或报告的 Host-side 项写「openCustomDialog().then 里 focusControl.requestFocus(<组件 id>) 兜底」；写错：宿主页 openCustomDialog(...) 之后没有 .then(() => focusControl.requestFocus(...))，弹层打开后输入框没有获焦

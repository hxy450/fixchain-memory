# EditText 的 inputType、InputFilter 和分段着色

agent 会看到什么：读到布局里 EditText 带 textCapCharacters、numberSigned 等 inputType 标志或 android:digits、maxLength，代码里挂 InputFilter.AllCaps，或以 BufferType.SPANNABLE 放入分段着色的文本；规格写「大写过滤」「无直接等价、放到校验时」「TextArea + Span」这类说法

## 规矩

- rule-b7de59c5419a｜规格逐个列 EditText 的 inputType 等到目标属性，键盘提示和内容约束分开｜读到：布局里的 EditText 带 textCapCharacters、textNoSuggestions、number、numberSigned 等 inputType 标志，可能另有 android:digits、maxLength；写错：规格把 textCapCharacters 写成「大写过滤」「文本过滤转大写」、写「textCapCharacters 无对应」，把 numberSigned 写成 InputType.Number，或只写「输入过滤在 Service 校验」而没有键盘映射
- rule-de767d978925｜规格把 InputFilter.AllCaps 写成「无直接等价、放到校验时大写化」时，改写成输入时拦截｜读到：源码里 EditText 挂 InputFilter.AllCaps；写错：规格的转换决策写「ArkUI 无直接等价，校验/大写化放 ViewModel」，把输入时的过滤降级成保存或校验时
- rule-55dc2dd4e3bc｜可编辑又分段着色的 EditText，规格映射到 RichEditor，不写 TextArea 加 Span｜读到：源码里同一个 EditText（含 AppCompatEditText）常驻可编辑，又以 setText(text, BufferType.SPANNABLE) 放入分段着色的 Spannable；写错：规格的转换决策写「TextArea + 着色用分段 Span 还原」这类组件不支持的组合，或写成只读 Text 与编辑框切换
- rule-16b2b899adeb｜规格里 textPassword 写「密码掩码、无显隐按钮 → showPasswordIcon(false)」｜读到：源端 EditText 只写 android:inputType="textPassword" 和 hint，布局里没有任何显示密码的切换控件；写错：规格转换决策写「TextInput({ type: InputType.Password }) + showPasswordIcon，HarmonyOS 自带显隐眼睛」，把源端没有的眼睛按钮当成对应物

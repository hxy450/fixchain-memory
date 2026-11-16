# 定长格子密码框（EditText 子类叠掩码格）

agent 会看到什么：读过的源码里格子式密码输入控件是 EditText 子类，写死 dp 宽高、带 maxLength、focusableInTouchMode，输满即在 OnTextChangeListener 里比对；交回的透明 TextInput 没设尺寸、被 HitTestMode.None 的掩码层挡住点不到，或改成了确定按钮提交

## 规矩

- rule-f1191269f2ef｜透明 TextInput 叠在掩码格上时，显式设成源控件尺寸或铺满 Stack｜读到：格子式密码输入控件（EditText 子类）在布局 XML 里写死 android:layout_width / android:layout_height（dp），带 android:maxLength、android:inputType="number"、android:focusableInTouchMode；写错：Stack 里的透明 TextInput 只设了透明 fontColor / backgroundColor 和 padding(0)，修饰链里没有 width / height，注释却写「覆在格子上承接点击」
- rule-8b5db511f38c｜掩码层设 HitTestMode.None 盖住透明输入框时，改由掩码层 onClick 去 requestFocus｜读到：源端整个格区就是一个可点的 EditText（android:focusableInTouchMode），点格区就弹键盘；写错：掩码格 Row 设 .hitTestBehavior(HitTestMode.None)，下层 TextInput 没铺满格区，外层卡片 Column 带吞点击的空 onClick，点格区没反应
- rule-c2c51173c169｜定长格子密码框输满即校验时，目标在 onChange 里按位数自动比对，不加确定按钮｜读到：源端定长格子密码框（MNPasswordEditText 一类）的 OnTextChangeListener 在 isComplete 时比对存储密码，else 分支 Toast 失败文案；写错：目标用普通 TextInput({ type: InputType.Password }) 加“确定” Button 提交比对，或注释写“源端不匹配无提示”而没有失败反馈

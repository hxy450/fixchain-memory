# 规格里 textPassword 写「密码掩码、无显隐按钮 → showPasswordIcon(false)」

审的是：规格
触发（任一种）：
- 读到：源端 EditText 只写 android:inputType="textPassword" 和 hint，布局里没有任何显示密码的切换控件；写错的样子：规格转换决策写「TextInput({ type: InputType.Password }) + showPasswordIcon，HarmonyOS 自带显隐眼睛」，把源端没有的眼睛按钮当成对应物
适用范围：规格提取阶段给密码输入框写转换决策时
做法：
- 转换决策写「密码掩码、无显隐按钮 → TextInput({ type: InputType.Password }).showPasswordIcon(false)」；源端确有显隐控件时才写显隐
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- showPasswordIcon(value: boolean): TextInputAttribute，默认 true：不写就会出现眼睛按钮，规格要写明 false（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputAttribute.showPasswordIcon）
来源：1 张卡，1 个应用
- case-9174c62c22f8d979372e（omni-notes-hmos）：做法第 1 步 ← 建议 1

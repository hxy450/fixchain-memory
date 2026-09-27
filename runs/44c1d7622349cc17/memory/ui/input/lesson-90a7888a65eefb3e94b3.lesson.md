# 透明 TextInput 叠在掩码格上时，输入层铺满格区并显式获焦，多段输入各用独立节点

ID：`lesson-90a7888a65eefb3e94b3` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段，把格子式密码框等自定义输入控件转成“透明 TextInput + 掩码格”叠层时

## 适用情境

源端弹窗内是固定尺寸的格子式输入控件（如 4 位数字密码），多段流程（设置、再次确认）各弹独立 Dialog 并各带新输入框；目标用页内条件挂载的浮层，透明 TextInput 与掩码 Row 叠放，外层卡片有吞点击的 onClick。

## 原因

透明 TextInput 不设宽高时按内容宽度约为 0，掩码层设 HitTestMode.None 放行后点击仍落不到输入框，被外层卡片吞掉；defaultFocus 对条件挂载的子树不生效，键盘不会自动弹出。来源修复中还观察到持焦状态下再点输入框不会重新拉起输入法、多段共用一个受控节点并在 onChange 同拍清空会失联（未单独验证）。

## 做法

1. 给 TextInput 显式设为源控件尺寸或铺满 Stack，写完核对完整修饰链，不以注释“覆在格子上”代替。
2. 逐层确认点击落点：上层放行后，下层输入框的边界是否覆盖整个格区，父容器吞点击的 onClick 会不会接住落空的点按。
3. 条件挂载的弹窗给输入框设 key，在 onAppear 中 requestFocus；格区点击也显式 requestFocus，键盘收起后可以再拉起。
4. 源端多段是独立 Dialog 时，目标按段拆成独立分支节点（可共用 builder），不用阶段标志复用同一受控输入。

## 来源（按需复核）

经验是有适用范围的历史建议。核查来源时同时看结论与 unknown；来源卡未随阅读包复制。

- case-1822d49fe750e20bd3be · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`8d82315e27d451acd40b24c5e74b6a36e16aa35c3f0093c7d7c8b01f589cca8a`

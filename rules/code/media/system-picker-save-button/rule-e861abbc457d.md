# 源端取 DISPLAY_NAME 作文件名时，目标对 picker URI 去 query/fragment 后解码末段

审的是：代码
触发（任一种）：
- 读到：源端取导入文件名走 ContentResolver 查 OpenableColumns.DISPLAY_NAME 的 helper；写错的样子：文件名写成 uri.split('?')[0] 的末段（baseName），没有 decodeURIComponent
适用范围：目标用 DocumentViewPicker 返回的 URI 推文件显示名时
做法：
- 先去掉 URI 的 ?query 和 #fragment，取最后一个 / 之后的段，再 decodeURIComponent 得到显示名；文件名和落盘名都用它
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- DocumentViewPicker 返回的 file://docs URI 末段是百分号编码的显示名：不解码时中文或带空格的文件名按编码串落盘（出处：卡里修好并验证过）
- select(option?: DocumentSelectOptions): Promise<Array<string>>：选择器只返回 URI 字符串，显示名要从 URI 推（出处：鸿蒙 SDK 的 ets/api/@ohos.file.picker.d.ts，DocumentViewPicker.select）
来源：1 张卡，1 个应用
- case-ce5d3e2da2846b40767d（MifareClassicTool）：做法第 1 步 ← 建议 5、诊断；取值 1 ← 建议 5、诊断

# 源端建议文件名用本地化短日期时间时，目标照源格式生成再做 FAT 合法化

审的是：代码
触发（任一种）：
- 读到：源码建议文件名用 DateFormat.getDateTimeInstance(SHORT, SHORT, Locale.getDefault()) 格式化；写错的样子：目标文件名写成固定格式（如 yyyy-MM-dd_HH-mm），或直接把含 '/'、':' 的本地化串交给 newFileNames
适用范围：导出、备份的建议文件名交给保存选择器时
做法：
- 按源端的本地化短日期 + 短时间生成文件名，再把控制字符和 " * / : < > ? \ | DEL 换成 _（Android FAT 文件名合法化），作为 DocumentSaveOptions.newFileNames 传入
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 本地化 SHORT/SHORT 加 FAT 文件名合法化后保留源格式：修复后的写法（出处：卡里修好并验证过）
- buildValidFatFilename 把非法字符换成 "_"，空名或 "."、".." 返回 "(invalid)"，并截到 255 字节：合法化的完整规则（出处：android.os.FileUtils#buildValidFatFilename）
- DocumentSaveOptions.newFileNames?: Array<string>：建议文件名的传入处（出处：鸿蒙 SDK 的 ets/api/@ohos.file.picker.d.ts，picker.DocumentSaveOptions.newFileNames）
未核实：DocumentViewPicker.save 对含 '/' 的 newFileNames 的处理，卡里没有实测
来源：1 张卡，1 个应用
- case-7e6984a7fa6d5845737b（Cofi）：做法第 1 步 ← 诊断、建议 3；取值 1 ← 诊断

# 源端 CreateDocument 按 MIME 补后缀时，目标端 newFileNames 直接写带 .zip 的名字

审的是：代码
触发（任一种）：
- 读到：源端用 SAF 的 CreateDocument（MIME 为 application/zip）launch("<不带后缀的名字>") 让用户选导出位置；写错的样子：目标端 DocumentSaveOptions 的 newFileNames 照抄不带后缀的名字
适用范围：转写源端经系统文件选择器导出文件的文件名常量时
做法：
- 记下源端系统组件的隐式补全；目标 picker 不保证补后缀时，在 newFileNames 里直接写带 .zip 的名字
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 显示名没有与所请求 MIME 匹配的扩展名时，按该 MIME 的默认扩展名补上：源端 launch 时不带 .zip，落盘的文件仍是 .zip（出处：android.os.FileUtils#splitFileName）
- DocumentSaveOptions.newFileNames?: Array<string>；DocumentViewPicker.save(option?: DocumentSaveOptions): Promise<Array<string>>：目标端保存选择器的建议文件名（出处：鸿蒙 SDK 的 ets/api/@ohos.file.picker.d.ts，DocumentSaveOptions.newFileNames、DocumentViewPicker.save）
未核实：目标设备上不写 .zip 时导出文件是否真的缺后缀，卡里没有实测记录；声明里没写 picker 会不会按类型补后缀
来源：1 张卡，1 个应用
- case-087050b57a3e1a6ac4ce（jerboa）：做法第 1 步 ← 建议 4

# 源端对 listFiles 每项直接 new FileInputStream 时，目标遇非普通文件判失败，不静默跳过

审的是：代码
触发（任一种）：
- 读到：遍历 listFiles() 的每一项直接 new FileInputStream(file) 写进 ZipOutputStream，外层 catch 报错；写错的样子：目标遍历时 !stat.isFile() 就 continue 静默跳过非普通文件（目录等），导出照常成功
适用范围：源端遍历目录逐项读文件、遇到读不了的项整体失败的导出或备份实现
做法：
- 遍历时 fs.statSync(path).isFile() 为 false 的项按失败处理，抛出并走源端 catch 里的同一条错误提示，不 continue
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 打开目录时 throw new ErrnoException("open", EISDIR)（Java 不允许读目录）：源端 new FileInputStream 遇目录会抛异常，导出整体失败（出处：libcore.io.IoBridge#open）
- isFile(): boolean：Stat 判断是否普通文件（出处：鸿蒙 SDK 的 ets/api/@ohos.file.fs.d.ts，Stat.isFile）
- statSync(file: string | number): Stat：同步取文件状态（出处：鸿蒙 SDK 的 ets/api/@ohos.file.fs.d.ts，fs.statSync）
来源：1 张卡，1 个应用
- case-ce5d3e2da2846b40767d（MifareClassicTool）：做法第 1 步 ← 建议 4、诊断

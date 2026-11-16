# 源端覆盖写入时，moveFileSync 前显式处理已存在目标，建目录、删旧、移动分开 catch

审的是：代码
触发（任一种）：
- 读到：源码覆盖写入：下载库 ignoreFilePathOccupy()，或 file.exists() 后 delete() 再 copyTo(...)；写错的样子：目标 mkdirSync、moveFileSync / copyFileSync 共用一个 try，任何异常都返回空串走失败分支；moveFileSync 前没处理已存在的目标
适用范围：把源端的覆盖式下载、复制落盘翻译成 fileIo 的移动或复制时
做法：
- 移动前显式处理目标：if (fileIo.accessSync(dest)) { fileIo.unlinkSync(dest) } 再 fileIo.moveFileSync(src, dest)
- 建目录、删旧文件、移动或复制各自 try / catch 并分别记录，「已存在」这类可恢复的错误不判为下载或设置失败
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- moveFileSync(src: string, dest: string, mode?: number): void；mode 默认 0 覆盖同名文件，1 表示同名时抛异常：不要为了「强制覆盖」传 1（出处：鸿蒙 SDK 的 ets/api/@ohos.file.fs.d.ts，moveFileSync）
- copyFileSync(src: string | number, dest: string | number, mode?: number): void；mode 只支持 0，覆盖同名文件：复制默认就是覆盖（出处：鸿蒙 SDK 的 ets/api/@ohos.file.fs.d.ts，copyFileSync）
- unlinkSync(path: string): void：删除已存在的目标文件（出处：鸿蒙 SDK 的 ets/api/@ohos.file.fs.d.ts，unlinkSync）
- 修好后 mkdir 单独包 try 容错、move 前 unlinkSync 目标，两条链路真机保存成功：修好后的做法（出处：卡里修好并验证过）
- moveFile(src: string, dest: string, mode?: number): Promise<void>：同族接口：异步移动，mode 含义同 moveFileSync（出处：鸿蒙 SDK 的 ets/api/@ohos.file.fs.d.ts，moveFile）
未核实：moveFileSync 目标已存在导致的失败卡里没有单独复现，move 前 unlink 是防御补充
来源：1 张卡，1 个应用
- case-1a45c3a64c664128775e（免费来电多多）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；取值 4 ← 诊断

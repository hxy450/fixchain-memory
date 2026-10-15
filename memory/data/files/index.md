# data/files

文件系统操作与导入导出：fileIo 建目录、移动与复制在目标已存在时的行为与幂等写法；导入时的 OOM 兜底按读接口错误码处理而不加读前阈值，手写 zip 容器沿用源端压缩方式，DocumentViewPicker 的选择数量上限与显示名解码

[上一级](../index.md)

## 本级经验

- [fileIo.mkdirSync 对已存在目录会抛 13900015：翻译“确保目录存在”时先判断或只放过该错误码，覆盖写先处理已存在目标](lesson-3f6b5d0b0ea6806a1b0c.lesson.md)
  - 时机：数据与服务层实现阶段，把 Android 的建目录、文件移动/复制落盘步骤翻译成 @kit.CoreFileKit fileIo 调用时
  - 情境：源端用 createOrExistsDir、mkdirs、getExternalFilesDir 保证目录存在，并在同一固定目录内重复下载、复制或覆盖（ignoreFilePathOccupy、exists 后 delete 再 copyTo）；目标用 fileIo.mkdirSync / moveFileSync / copyFileSync 实现同一管线。
- [替换源端取文件显示名的 helper 前读完实现：picker URI 去掉 query 后对末段 decodeURIComponent](lesson-f22b8d9ae2c8a0d9db25.lesson.md)
  - 时机：页面与数据层实现阶段，把源端按 OpenableColumns.DISPLAY_NAME 取文件名的 helper（getFileName 一类）迁到目标，处理 DocumentViewPicker 返回的 URI 时
  - 情境：源端以 getFileName 一类 helper 查询 ContentResolver 的 OpenableColumns.DISPLAY_NAME，并按 URI scheme 分支处理；目标从 DocumentViewPicker 得到 file://docs/... 形式的 URI。
- [源端 ZipOutputStream 未 setMethod 时默认 DEFLATED：手写 zip 容器也用 deflate，不改成存储模式](lesson-53f654b625ab5a535955.lesson.md)
  - 时机：数据层实现阶段，把 ZipOutputStream 打包导出迁到目标，系统 zip 接口不满足要求而改手写容器时
  - 情境：源端用 java.util.zip.ZipOutputStream 写条目且未调用 setMethod；目标的 zlib 打包接口不能控制条目名或时间，准备手写 local header 与 central directory 的 zip 容器；源端遇到目录等不可读条目时抛错并提示失败。
  - 例外：源端显式 setMethod(ZipOutputStream.STORED) 时按存储模式写，并按 STORED 要求预先写入 CRC 与大小
- [源端只在 catch(OutOfMemoryError) 时提示文件过大：目标照常读取，读取或分配失败时再提示，不加读前大小阈值](lesson-8534b92df38e546092fe.lesson.md)
  - 时机：规格提取与数据层实现阶段，把导入、打开文件时的 OOM 兜底映射为目标读取与错误处理时
  - 情境：源端导入文件时直接整读，只在 catch (OutOfMemoryError) 分支提示“文件过大”，没有大小阈值；规格或派工可能把它写成“读前长度预检”或“文件大小上限校验”；目标用 @kit.CoreFileKit fileIo 读取。
  - 例外：当前任务明确批准设置大小上限：登记为有意偏离，写明数值来源
- [源端多选不限数量（EXTRA_ALLOW_MULTIPLE）时，DocumentViewPicker 显式设 maxSelectNumber 上限](lesson-b502dde7a358a0139527.lesson.md)
  - 时机：数据层与页面实现阶段，把源端系统文件选择器的多选迁到 DocumentViewPicker、设置 DocumentSelectOptions 时
  - 情境：源端以 ACTION_OPEN_DOCUMENT/ACTION_GET_CONTENT 加 EXTRA_ALLOW_MULTIPLE 选择文件，不限数量；目标用 DocumentViewPicker.select(DocumentSelectOptions)。

# data/files

文件系统操作与导入导出：fileIo 建目录、移动与复制在目标已存在时的行为与幂等写法；导入导出按源端运行时与库默认语义实现（OOM 兜底、选择数量上限、zip 压缩方式、picker 显示名解码）；源端后台线程里的拷贝与导入改用异步 IO 或 taskpool；OutputStream 覆盖写改 fileIo 时的 TRUNC、短写与字节视图切片

[上一级](../index.md)

## 本级经验

- [OutputStream 覆盖写改成 fileIo：打开加 TRUNC，按 writeSync 返回值写完，字节视图按偏移切出 ArrayBuffer](lesson-4c93cca5dde48080b008.lesson.md)
  - 时机：数据与服务层实现阶段，把 Java FileOutputStream/openOutputStream 加 write(data) 的整文件写入翻译为 fileIo.openSync/writeSync，或把 Uint8Array 字节交给要求 ArrayBuffer 的接口时
  - 情境：源端以非追加方式打开输出流后一次 write(data) 覆盖整个文件；目标照参考示例写 openSync(WRITE_ONLY | CREATE) 加一次 writeSync，示例针对新建文件与字符串内容；要写的字节可能是 subarray 视图（如元数据写入器返回的切片）。
- [fileIo.mkdirSync 对已存在目录会抛 13900015：翻译“确保目录存在”时先判断或只放过该错误码，覆盖写先处理已存在目标](lesson-3f6b5d0b0ea6806a1b0c.lesson.md)
  - 时机：数据与服务层实现阶段，把 Android 的建目录、文件移动/复制落盘步骤翻译成 @kit.CoreFileKit fileIo 调用时
  - 情境：源端用 createOrExistsDir、mkdirs、getExternalFilesDir 保证目录存在，并在同一固定目录内重复下载、复制或覆盖（ignoreFilePathOccupy、exists 后 delete 再 copyTo）；目标用 fileIo.mkdirSync / moveFileSync / copyFileSync 实现同一管线。
- [文件导入导出按源端运行时与库默认语义实现：OOM 兜底不改成读前大小阈值，无数量上限就取目标 API 最大值，ZipOutputStream 默认 DEFLATED，picker URI 末段解码后作显示名](lesson-8534b92df38e546092fe.lesson.md)
  - 时机：规格提取与数据层实现阶段，把源端导入导出的异常兜底、压缩流、系统选择器返回值与数量限制映射为目标平台实现时
  - 情境：Android 导入导出只在 catch(OutOfMemoryError) 时提示文件过大、没有大小阈值；用 ZipOutputStream 打包且未调用 setMethod；以 getFileName 一类 helper 取 DISPLAY_NAME；选择器用 EXTRA_ALLOW_MULTIPLE 不限数量。目标使用 DocumentViewPicker 返回的 URI，系统 zip API 不能控制 entry 名与时间而改手写容器；规格可能把 OOM 兜底写成“读前长度预检”，派工也写了“文件大小上限校验”。
  - 例外：确需上限或不同压缩方式时登记为有意偏离，并写明数值来源与可见影响
- [源端在后台线程执行的文件拷贝与导入改用异步 IO 或 taskpool：async 函数里调用 *Sync 接口仍阻塞主线程](lesson-ff5e8fbfb9ed491d99ee.lesson.md)
  - 时机：服务层实现阶段，把源端 AsyncTask、线程池或后台线程里的文件拷贝、读写与批量导入翻译为 ArkTS，并核对规格要求的并发或后台执行时
  - 情境：源端在 AsyncTask.doInBackground、executeOnExecutor(THREAD_POOL_EXECUTOR) 或 Executor 中拷贝附件、读写大文件，多个 URI 并行处理；规格或附录写明目标用 taskpool 并发、主线程只收束结果；实现者手里有 fileIo.copyFileSync、openSync/readSync 等同步接口。

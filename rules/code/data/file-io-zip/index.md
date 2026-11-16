# 文件读写、建目录和 ZIP 打包

agent 会看到什么：读到源端用 File.mkdirs / createOrExistsDir、FileInputStream、listFiles、ZipOutputStream.putNextEntry 和 catch (OutOfMemoryError) 读写文件、打包导出；产物里 fs / fileIo 的 mkdirSync、statSync、手写 ZIP 或 zlib 的对应写法

## 规矩

- rule-c32a3f0415b1｜源端 createOrExistsDir / mkdirs 建目录，目标保留「已存在即成功」，不裸调 mkdirSync｜读到：源码用 FileUtils.createOrExistsDir(dir)、File.mkdirs() 或 getExternalFilesDir("…") 保证目录存在，并在同一固定目录里重复下载、复制；写错：目标裸调 fileIo.mkdirSync(dir, true)，和后续 moveFileSync / copyFileSync 放在同一个 try 里，第二次执行抛 13900015 被当成下载或设置失败
- rule-23f9157c6ce9｜源端只在 OutOfMemoryError 时报文件过大：目标照常读、catch RangeError 再提示｜读到：catch (OutOfMemoryError e) 里提示文件过大，读之前没有大小判断；写错：读前用 fs.stat(...) / fs.statSync(...) 比较 size，超出自定上限（如 16 MiB）就拒读，替换了 try/catch
- rule-a1c6cf381fa0｜源端对 listFiles 每项直接 new FileInputStream 时，目标遇非普通文件判失败，不静默跳过｜读到：遍历 listFiles() 的每一项直接 new FileInputStream(file) 写进 ZipOutputStream，外层 catch 报错；写错：目标遍历时 !stat.isFile() 就 continue 静默跳过非普通文件（目录等），导出照常成功
- rule-52aa00293fb1｜ZipOutputStream 没调 setMethod 时，手写 ZIP 按 DEFLATED 加数据描述符｜读到：new ZipOutputStream(...) 后 putNextEntry 写条目，没有调用 setMethod 或 ZipEntry.setMethod；写错：因 zlib.zipFile / compressFile 控制不了条目名和时间而手写 ZIP 容器，条目写成 STORED（method 0，不压缩）
- rule-0c3ed35405ed｜源端覆盖写入时，moveFileSync 前显式处理已存在目标，建目录、删旧、移动分开 catch｜读到：源码覆盖写入：下载库 ignoreFilePathOccupy()，或 file.exists() 后 delete() 再 copyTo(...)；写错：目标 mkdirSync、moveFileSync / copyFileSync 共用一个 try，任何异常都返回空串走失败分支；moveFileSync 前没处理已存在的目标
- rule-c263207ee75f｜FileOutputStream 覆盖写迁成 fileIo 时，加 TRUNC 并按 writeSync 返回值写完｜读到：源端 new FileOutputStream(file) 或 openOutputStream(uri) 加 OutputStream.write(data) 整文件写入；写错：fileIo.openSync(path, OpenMode.WRITE_ONLY | OpenMode.CREATE) 没有 TRUNC，只调一次 writeSync 且不检查返回的字节数
- rule-7433153a60d5｜picker 返回的 URI 先 fileIo.openSync 取 fd，再交给 copyFileSync｜写错：fileIo.copyFileSync(源路径, uri)：DocumentViewPicker 或媒体库返回的 URI 被直接当成目标路径传给 copyFileSync
- rule-5aa60c990460｜Uint8Array 交给写入接口时按 byteOffset/byteLength 切片，不直接传 .buffer｜读到：字节以 Uint8Array 视图传递，可能是 subarray 等返回的视图（如 EXIF 处理后的结果）；写错：写入或提交媒体资源时直接传 bytes.buffer
- rule-34d1ce8da1f4｜备份归档的条目名常量照源端 Room 库文件名写，不带 .db｜读到：源端 Room.databaseBuilder(context, klass, name) 的 name 没有 .db；写错：目标端备份代码里 zip 条目名常量写成带 .db 的名字（注释引规格的工件契约），压缩时按这个名归档
- rule-6e5bab0feb44｜源端靠 GZIPInputStream 抛异常判损坏时，目标在 gzopen 前先校验魔数 1f 8b｜读到：源端用 `GZIPInputStream` 读压缩内容，catch 到异常就返回加载失败态；写错：目标用 zlib 的 gzopen(path, 'rb') + gzread 直接解压、没校验格式，注释却写「损坏时抛错」；调用方只靠 catch 判损坏
- rule-47751a57bb58｜规格写了后台或并发拷贝时，拷贝用 fileIo 的异步 API，不用 *Sync 再包 async｜读到：源端在 AsyncTask.executeOnExecutor(THREAD_POOL_EXECUTOR) 的 doInBackground 里拷贝文件；规格或 addendum 写「taskpool.execute 并发 + 主线程收束」「逐个并发创建任务（多 uri 并行拷贝）」；写错：拷贝链写成 fileIo.copyFileSync、fileIo.openSync + readSync 同步 IO，外面只包一层 async 函数

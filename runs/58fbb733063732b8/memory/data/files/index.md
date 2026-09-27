# data/files

文件系统操作：fileIo 建目录、移动与复制在目标已存在时的行为与幂等写法

[上一级](../index.md)

## 本级经验

- [fileIo.mkdirSync 对已存在目录会抛 13900015：翻译“确保目录存在”时先判断或只放过该错误码，覆盖写先处理已存在目标](lesson-3f6b5d0b0ea6806a1b0c.lesson.md)
  - 时机：数据与服务层实现阶段，把 Android 的建目录、文件移动/复制落盘步骤翻译成 @kit.CoreFileKit fileIo 调用时
  - 情境：源端用 createOrExistsDir、mkdirs、getExternalFilesDir 保证目录存在，并在同一固定目录内重复下载、复制或覆盖（ignoreFilePathOccupy、exists 后 delete 再 copyTo）；目标用 fileIo.mkdirSync / moveFileSync / copyFileSync 实现同一管线。

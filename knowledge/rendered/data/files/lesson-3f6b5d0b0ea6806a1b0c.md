# fileIo.mkdirSync 对已存在目录会抛 13900015：翻译“确保目录存在”时先判断或只放过该错误码，覆盖写先处理已存在目标

## 何时使用

数据与服务层实现阶段，把 Android 的建目录、文件移动/复制落盘步骤翻译成 @kit.CoreFileKit fileIo 调用时

## 适用情境

源端用 createOrExistsDir、mkdirs、getExternalFilesDir 保证目录存在，并在同一固定目录内重复下载、复制或覆盖（ignoreFilePathOccupy、exists 后 delete 再 copyTo）；目标用 fileIo.mkdirSync / moveFileSync / copyFileSync 实现同一管线。源端在同名非空文件已存在时直接复用、不再下载的短路分支要照样保留：第 2 步的删旧覆盖只用于源端确实覆盖写入的那一步，不改成每次都删旧重下。

## 原因

mkdirSync(dir, true) 的“递归”不等于“已存在即成功”，目录已存在时抛 13900015；moveFileSync 默认 mode 为 0，目标位置已有同名文件时强制覆盖，只有传 mode 1 才会因同名抛异常。建目录、删旧文件、移动放在同一个 try 里时，第二次执行必然走进失败分支（报“下载失败”）。来源中生成者读到的源码表明目录会复用，但所加载的下载 skill 把裸 mkdirSync(dir, true) 写成标准步骤，错误码表只列了目录不存在的情况。

## 做法

1. 翻译“确保目录存在”时先用 fileIo.accessSync(dir) 判断，或只在捕获 code 13900015 时继续，不把 mkdirSync(dir, true) 当作幂等调用。
2. 源端是覆盖写入时，移动或复制前显式处理已存在目标（unlinkSync 或确认 mode 语义）；把建目录、删旧、移动分开处理和记录，避免一个 catch 把可恢复的“已存在”判为整链失败。
3. 在固定目录里重复执行的下载、设置链，写完按“第二次执行、目录与同名文件都已存在”走查一遍。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕fileIo.mkdirSync(path, true) 在目录已存在时抛 BusinessError 13900015（File exists），recursion 为 true 不会让“已存在”算成功
- 〔做法第 1 步〕fileIo.accessSync(path) 不传 mode 时按 AccessModeType.EXIST 检查文件或目录是否存在，返回 boolean
- 〔原因 / 做法第 2 步〕fileIo.moveFileSync 的 mode 默认 0：移动位置已有同名文件时强制覆盖；mode 为 1 时遇同名文件抛异常
- 〔做法第 2 步〕fileIo.copyFileSync 的 mode 只支持 0（也是默认值）：完全覆盖目标文件，未覆盖的部分被裁剪掉
- 〔适用情境〕java.io.File#mkdirs 在目录已存在时直接返回 false，不抛异常

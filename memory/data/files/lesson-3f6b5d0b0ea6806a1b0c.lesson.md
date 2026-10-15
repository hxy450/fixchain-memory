# fileIo.mkdirSync 对已存在目录会抛 13900015：翻译“确保目录存在”时先判断或只放过该错误码，覆盖写先处理已存在目标

ID：`lesson-3f6b5d0b0ea6806a1b0c` · 版本：3

[本主题](index.md)

## 何时使用

数据与服务层实现阶段，把 Android 的建目录、文件移动/复制落盘步骤翻译成 @kit.CoreFileKit fileIo 调用时

## 适用情境

源端用 createOrExistsDir、mkdirs、getExternalFilesDir 保证目录存在，并在同一固定目录内重复下载、复制或覆盖（ignoreFilePathOccupy、exists 后 delete 再 copyTo）；目标用 fileIo.mkdirSync / moveFileSync / copyFileSync 实现同一管线。

## 原因

mkdirSync(dir, true) 的“递归”不等于“已存在即成功”：@ohos.file.fs.d.ts 中 mkdirSync(path, recursion) 声明 13900015 File exists，目录已存在时传 true 也会抛出。移动与复制的覆盖行为由 mode 决定：同一 d.ts 中 moveFileSync 的 mode 默认 0、覆盖同名文件，传 1 才在目标存在时抛错；copyFileSync 只支持 mode 0（覆盖）。参考模板常把裸 mkdirSync(dir, true) 写成幂等步骤；建目录、删旧文件、移动放在同一个 try 里时，第二次执行会因建目录抛错走进失败分支。

## 做法

1. 翻译“确保目录存在”时先用 fileIo.accessSync(dir) 判断，或只在捕获 code 13900015 时继续，不把 mkdirSync(dir, true) 当作幂等调用。
2. 源端是覆盖写入时，移动或复制前确认已存在目标的处理：moveFileSync 保持 mode 0（默认覆盖），不改成 1；源端先删后写时先 unlinkSync 目标。把建目录、删旧、移动分开处理和记录，避免一个 catch 把可恢复的“已存在”判为整链失败。
3. 在固定目录里重复执行的下载、设置链，写完按“第二次执行、目录与同名文件都已存在”走查一遍。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-1a45c3a64c664128775e](../../../store/cases/case-1a45c3a64c664128775e/1b2dcb8f0690a65d2e7512b4157ddffe7ada585da58cef24f9f7ef50fe96fe5a.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`1b2dcb8f0690a65d2e7512b4157ddffe7ada585da58cef24f9f7ef50fe96fe5a`

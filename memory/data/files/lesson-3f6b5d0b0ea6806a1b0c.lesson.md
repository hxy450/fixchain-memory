# fileIo.mkdirSync 对已存在目录会抛 13900015：翻译“确保目录存在”时先判断或只放过该错误码，覆盖写先处理已存在目标

ID：`lesson-3f6b5d0b0ea6806a1b0c` · 版本：2

[本主题](index.md)

## 何时使用

数据与服务层实现阶段，把 Android 的建目录、文件移动/复制落盘步骤翻译成 @kit.CoreFileKit fileIo 调用时

## 适用情境

源端用 createOrExistsDir、mkdirs、getExternalFilesDir 保证目录存在，并在同一固定目录内重复下载、复制或覆盖（ignoreFilePathOccupy、exists 后 delete 再 copyTo）；目标用 fileIo.mkdirSync / moveFileSync / copyFileSync 实现同一管线。

## 原因

mkdirSync(dir, true) 的“递归”不等于“已存在即成功”，目录已存在时抛 13900015；当前官方 moveFileSync 的 mode 默认 0，同名时强制覆盖；mode 1 才对同名目标抛异常，不能把建目录失败推成移动默认不覆盖。这些操作共用一个 try 时，前面的建目录异常可能提前终止整条链；应记录具体失败操作，不能只凭“第二次下载失败”判断移动模式。来源中生成者读到的源码表明目录会复用，但所加载的下载 skill 把裸 mkdirSync(dir, true) 写成标准步骤，错误码表只列了目录不存在的情况。

## 做法

1. 翻译“确保目录存在”时先用 fileIo.accessSync(dir) 判断，或只在捕获 code 13900015 时继续，不把 mkdirSync(dir, true) 当作幂等调用。
2. 源端是覆盖写入时，分别核移动和复制的同名策略；moveFileSync 可按源策略显式选 mode 0 覆盖或 mode 1 拒绝，不能把 unlinkSync 当作默认覆盖必需步骤；把建目录、删旧、移动分开处理和记录，避免一个 catch 把可恢复的“已存在”判为整链失败。
3. 在固定目录里重复执行的下载、设置链，写完按“第二次执行、目录与同名文件都已存在”走查一遍。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-1a45c3a64c664128775e](../../../store/cases/case-1a45c3a64c664128775e/1b2dcb8f0690a65d2e7512b4157ddffe7ada585da58cef24f9f7ef50fe96fe5a.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`1b2dcb8f0690a65d2e7512b4157ddffe7ada585da58cef24f9f7ef50fe96fe5a`

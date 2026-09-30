# Windows PowerShell 5.1 读取 UTF-8 中文规格、账本与源码要显式 -Encoding UTF8；回执出现乱码就当作没读

ID：`lesson-6a3a7f46c8fec282affa` · 版本：2

[本主题](index.md)

## 何时使用

规格提取、切片实现与接线阶段，在 Windows PowerShell 5.1 下用 Get-Content/Select-String 读取功能规格、决策账本或中文注释源码时；诊断与返修时据读取回执判断代码结构时

## 适用情境

迁移工程的规格、决策账本、计划与源码为 UTF-8（无 BOM）且含中文；读取者在 Windows PowerShell 5.1 中不带编码参数读取，回执里中文段落变成成片乱码，AC 编号、方法名、路径等 ASCII 片段仍然可读，含中文注释的代码行可能与下一行连在一起。

## 原因

Windows PowerShell 5.1 的 Get-Content/Select-String 默认按系统 ANSI 代码页解码无 BOM 的 UTF-8 文件，中文条款变成乱码而 ASCII 标识照常显示，读取者容易以为已经读到了条款。来源为同一应用的多次切片实现：实现者读到的功能规格中文正文均为乱码，只凭 AC 编号与方法名实现，漏掉了“成功后才写缓存”“先授权再定位、拒绝不能静默”“登录成功后重载任务数据”等只写在中文正文里的条件。同样的误解码还会吞掉中文注释行尾的换行，使下一行代码显示在注释后面；另一应用的返修者据此误判权限判断“被乱码注释吞掉”，按合并后的行写的补丁找不到上下文。

## 做法

1. 在 PowerShell 5.1 中读取文本一律带编码：Get-Content -Raw -Encoding UTF8、Select-String -Encoding UTF8；批量读取前也可先设置 $OutputEncoding = [Console]::OutputEncoding = [Text.UTF8Encoding]::new()。
2. 回执里出现成片乱码时，把该文件视为未读，用 UTF-8 重读后再据此实现；不要凭可读的 AC 编号、方法名推断条款内容。
3. 乱码回执里代码看似并入注释行时，先用 UTF-8 重读，或以 analyzer 行号、补丁上下文核对原文件的行结构，再判断代码是否真被注释。


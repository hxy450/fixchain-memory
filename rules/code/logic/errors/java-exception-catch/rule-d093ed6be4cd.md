# 实现兜底/继续类 AC 时，只兜源码 catch 的异常，null 解引用处抛出终止任务

审的是：代码
触发（任一种）：
- 读到：Java 源码只 `catch (IOException e)` 返回空对象，解析异常（Gson JsonSyntaxException）不在其内；对 `findFile(...)` 等可能为 null 的返回值直接解引用；写错的样子：ArkTS 把 `JSON.parse` 包进 try/catch，失败后 hilog.error 并返回空对象继续；目录不存在时 `return false`，随后照样走后续步骤并发完成通知
适用范围：实现规格里「兜底/不崩溃/继续处理其余文件」一类 AC，或转写源码的异常和 null 分支时
做法：
- 只对源码 catch 的那类异常兜底：源码只 catch IOException 时，JSON 语法错误不 catch，向上抛出
- 源码对可能为 null 的返回值直接解引用的，目标在同一处 throw 一个错误终止任务，不 return false 后继续后续步骤和完成通知
- 规格写「保持 parity」却把结局写成「继续」时，按源码结局写，并在交回里回报规格缺口
来源：1 张卡，1 个应用
- case-3cdc388116566cb08735（omni-notes-hmos）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2、诊断；做法第 3 步 ← 建议 5

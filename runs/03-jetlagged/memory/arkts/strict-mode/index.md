# arkts/strict-mode

ArkTS 严格模式对写法的限制（throw、类型收窄等），在不编译的生成批次里容易留到编译门

[上一级](../index.md)

## 本级经验

- [catch 中继续抛出时先把异常收窄为 Error，不直接 throw catch 变量](lesson-dbfae443e671c568e14e.lesson.md)
  - 时机：功能实现或修复阶段，在 try/catch 中决定把捕获到的异常继续向上抛出时
  - 情境：ArkTS 严格模式工程中，catch 分支需要把当前任务的异常继续上报（例如过期任务的异常按取消处理、当前任务的异常上报），catch 变量没有 Error 类型保证；写码批次按约束不自行编译，或修改落在组编译之后。
  - 例外：抛出的值已经在同一分支里由 instanceof Error 等判断收窄为 Error

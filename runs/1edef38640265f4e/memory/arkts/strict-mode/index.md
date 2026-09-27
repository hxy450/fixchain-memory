# arkts/strict-mode

ArkTS 严格模式对写法的限制（throw、对象字面量类型、索引签名、类型收窄等），在不编译的生成批次或未接线文件里容易留到编译门

[上一级](../index.md)

## 本级经验

- [ArkTS 里给对象字面量写显式 class/interface 类型；去掉 Record 时键已知用具名字段类、键不定用 Map，不改成索引签名](lesson-1696967d1320c7735732.lesson.md)
  - 时机：编码或返修阶段，为一组命名常量、主题令牌或键值集合确定类型声明，或按规范替换 Record/Object 时
  - 情境：代码用对象字面量承载间距、圆角等令牌，或用键值集合保存偏好、设置；目标文件可能还没被页面或 Ability 导入，或者并发 worker 被要求不跑全量构建，编译器暂时检查不到这些写法。
- [catch 中继续抛出时先把异常收窄为 Error，不直接 throw catch 变量](lesson-dbfae443e671c568e14e.lesson.md)
  - 时机：功能实现或修复阶段，在 try/catch 中决定把捕获到的异常继续向上抛出时
  - 情境：ArkTS 严格模式工程中，catch 分支需要把当前任务的异常继续上报（例如过期任务的异常按取消处理、当前任务的异常上报），catch 变量没有 Error 类型保证；写码批次按约束不自行编译，或修改落在组编译之后。
  - 例外：抛出的值已经在同一分支里由 instanceof Error 等判断收窄为 Error

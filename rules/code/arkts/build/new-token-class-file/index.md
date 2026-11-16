# 新建的主题令牌、常量类 .ets 文件

agent 会看到什么：读到派工要求新建主题令牌类（DesignTokens 一类）或示例用 static readonly X = { … } 承载令牌；交回的令牌类写了无类型的对象字面量，或新文件没被任何页面 import 却报告全量构建通过

## 规矩

- rule-f41f4e74b39f｜令牌或常量类的对象字面量要有显式 class 或 interface 类型，不照搬无类型示例｜读到：示例或参考里用 `static readonly X = { a: …, b: … }` 承载主题令牌（间距、圆角等）；写错：新建的令牌类里写 `static readonly spacing = { … }` 这类没声明类型的对象字面量（编译报 `arkts-no-untyped-obj-literals`）
- rule-058dbc7c41e3｜新建但没被页面或 Ability 导入的 .ets 不进全量编译，报告构建通过前先接一处导入或单独检查｜读到：派工要求输出新的 .ets（如主题令牌类），或要求 worker 不跑全量构建；写错：新建的 .ets 没有被任何 @Entry 页面或 UIAbility 链路 import，报告却写全量构建通过

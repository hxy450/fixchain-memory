# 令牌或常量类的对象字面量要有显式 class 或 interface 类型，不照搬无类型示例

审的是：代码
触发（任一种）：
- 读到：示例或参考里用 `static readonly X = { a: …, b: … }` 承载主题令牌（间距、圆角等）；写错的样子：新建的令牌类里写 `static readonly spacing = { … }` 这类没声明类型的对象字面量（编译报 `arkts-no-untyped-obj-literals`）
适用范围：编码阶段新建主题令牌、常量集合这类用对象字面量承载一组命名值的 .ets 文件
做法：
- 每组令牌先声明一个具名 class 或 interface（字段带类型），常量写成 static readonly 名字: 该类型 = …，不写无类型的 { … }
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- arkts-no-untyped-obj-literals（错误码 10605038）：需要显式标注对象字面量的类型：无类型的对象字面量是编译错误（出处：typescript-to-arkts-migration-guide.md，需要显式标注对象字面量的类型）
- 不能用字面量初始化带 readonly 字段的类、带方法的类或接口、带含参构造函数的类：令牌类型的字段若写成 readonly，常量要用 new 构造，不能用 { … } 赋值（出处：typescript-to-arkts-migration-guide.md，需要显式标注对象字面量的类型）
- 改成具名的令牌类后这两处编译错误消失：修好的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-98e7bd27bb334db83f51（Cofi）：做法第 1 步 ← 建议 1、诊断；取值 3 ← 诊断

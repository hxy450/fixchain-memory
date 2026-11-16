# AppStorageV2 / PersistenceV2 的 connect 调用

agent 会看到什么：产物里 AppStorageV2.connect、PersistenceV2.connect / globalConnect 的 key 写法和放在 static 初始化器里的调用，以及该取共享实例的页面 new 了私有实例

## 规矩

- rule-8c7319edc18b｜模型要被其他页面读写时，页面从一开始用 AppStorageV2.connect 取共享实例，不 new 私有实例｜读到：规格或决策写某个模型要被其他功能或页面读写（如「向 F003 提供候选数据」）；写错：页面里 `@Local model = new …(...)` 自己创建私有实例，另一个页面用 AppStorageV2.connect 取到的是另一份
- rule-08333c281fed｜AppStorageV2/PersistenceV2 的 key 只用字母、数字、下划线，连字符和点号换成下划线｜读到：工程模块文件名用 kebab-case，状态管理参考只给了 `AppStorageV2.connect(Cls, key, …)` 签名；写错：`AppStorageV2.connect(Cls, '…-…', …)` 或 PersistenceV2 的 key 含连字符（照文件名连字符化写的）
- rule-7a6e7dcff9cc｜static 字段初始化器或模块级常量把类当值用时，这个类要声明在使用者之上或从别的文件 import｜写错：服务类里 `static readonly x: S = AppStorageV2.connect(S, KEY, () => new S())!`、PersistenceV2.globalConnect({ type: S, … }) 或 `static … = new S()`，而 @ObservedV2 class S 声明在同一文件的服务类下方；编译报 Class 'S' used before its declaration
- rule-c736d0998f55｜AppStorageV2.connect 返回 T | undefined，读写前先判空｜读到：源端用全局单例、Application 字段或 Intent extras 暂存跨页数据，规格或 pitfall 给出 AppStorageV2.connect(Cls, key, () => new Cls()) 写法；写错：const x = AppStorageV2.connect(...) 后直接写 x.字段 = …，没有 undefined 守卫，严格空检查报 possibly 'undefined'

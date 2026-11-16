# Tab 标签、页面标题、设置行等可见文案，沿源端资源引用链取 strings.xml 逐字值

审的是：代码
触发（任一种）：
- 读到：源端可见文案经资源键间接引用：导航目的地枚举的 label = Res.string.xxx、路由的标题资源、顶部栏 title = stringResource(Res.string.xxx)；写错的样子：Tab 标签、路由标题、设置入口行写成枚举名或路由名（如 Text('Map')、Text('Messages')）或自拟英文（'User Config'），和 strings.xml 的逐字值不同
- 读到：已读的 brief 或页面 spec 逐字给出了屏幕标题、入口行和摘要（如 `Res.string.xxx = "…"`）；写错的样子：写出的 Text('…') 或路由表标题和 brief 给的字面值不同，或摘要里删掉了括号内容
适用范围：界面实现阶段给 Tab 标签、页面和路由标题、设置入口行等可见文案取值，写进页面和路由表时
做法：
- 沿引用链把每个可见文案解析到 strings.xml 的逐字值（枚举 label → Res.string 键 → `<string name="键">` 的内容）；已读 brief 或页面 spec 给出字面值的直接照抄，不用卡片标题、路由名或枚举名替代，也不删改括号内容
- 把这批可见文案集中到一个常量或资源文件，每项注明源资源键，页面和路由表只引用它；提交前用源 strings.xml 对这个文件逐项比对
- 页面 spec 与实现并行时，实现某页前先读该页 spec 的标题和顶部栏行，不以自建资源表代替
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 可见文案集中到常量文件作单一来源、按 AC 程序化对照 strings.xml 后，Tab、路由标题、设置行与源端一致：修好后的做法（出处：卡里修好并验证过）
针对本应用要查的：
- 每个可见文案的逐字值：源工程的 strings.xml（Compose Multiplatform 在 composeResources/values/ 下，Android 在 res/values/ 下），按 Res.string 或 R.string 后的键名找 `<string name>`；原样抄 value，含括号、大小写和标点；引用的是枚举或路由时先在源码里找到它对应的资源键
来源：1 张卡，1 个应用
- case-6bfa66c963473bc7bea1（Meshtastic）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2、诊断；做法第 3 步 ← 建议 3；取值 1 ← 诊断

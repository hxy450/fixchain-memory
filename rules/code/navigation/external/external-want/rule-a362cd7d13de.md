# 补齐缺失服务时先读 spec 的 AC 和源码锚点，不按调用点补 void 加静默 catch 的空壳

审的是：代码
触发（任一种）：
- 读到：检查器报切片自有服务缺失或未实例化（如「does not instantiate」），手里只有调用点名如 X.open(url)；源端打开链接的工具里 startActivity 捕获 ActivityNotFoundException、mailto 走邮件、custom tab 分支；写错的样子：补出的 open(context, url): void 把 startAbility 失败静默 catch，没有空串和 # 守卫、mailto 分支、返回值、失败提示和异常分类，注释却写「与 Android 的 ActivityNotFound 兜底一致」
- 写错的样子：沿用空壳再加一个只委托 this.open(...) 的方法（如 custom tab 入口），没有返回值和异常分类，页面也接到它上面
适用范围：group closer 或后续写者补齐切片自有服务、或给已有空壳加入口时
做法：
- 先读该符号在功能 spec 里的 AC 和源码锚点（打开链接工具里 startActivity、custom tab 那几个方法），按契约实现返回值、空白/锚点守卫、失败提示和异常分类
- 读不到契约就退回切片补做；不写 void 加静默 catch 的空壳，不在注释里声称与源码一致
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- startAbility(want: Want, options?: StartOptions): Promise<void>：UIAbilityContext 启动其它应用，失败以 BusinessError 拒绝（出处：鸿蒙 SDK 的 ets/api/application/UIAbilityContext.d.ts，UIAbilityContext.startAbility）
- 16000019：No matching ability is found（隐式启动未查找到匹配应用）：没有能处理该链接的应用时的错误码，异常分类时与其它错误分开（出处：鸿蒙 SDK 的 ets/api/application/UIAbilityContext.d.ts，UIAbilityContext.startAbility；errorcode-ability.md，16000019）
- 重写为：构造 Want 前做守卫、mailto 分支、open 返回 boolean 并在失败时提示、custom tab 入口带异常分类：修法（出处：卡里修好并验证过）
- startAbility(want: Want, options?: StartOptions): Promise<void>：同族接口：UIExtensionContext 的同名方法（出处：鸿蒙 SDK 的 ets/api/application/UIExtensionContext.d.ts，UIExtensionContext.startAbility）
针对本应用要查的：
- 该服务的行为契约：功能 spec 里标了该符号的 AC，以及源工程里对应工具类的方法体；逐条读出返回值、守卫条件、提示文案的资源名和异常分类，照写到目标
来源：1 张卡，1 个应用
- case-85c033903030498c795d（com.nononsenseapps.feeder）：做法第 1 步 ← 建议 4；做法第 2 步 ← 建议 4；取值 3 ← 诊断

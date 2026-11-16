# 源端文案带格式参数时，读出资源模板的占位符和代入点，目标按序传参给 $r

审的是：代码
触发（任一种）：
- 读到：源端 getString(R.string.…, a)、stringResource(R.string.…, a, b)，或 android:summary 引用的串里有 %s、%1$s 占位；写错的样子：目标 $r('app.string.…') 不传参（界面显示 %1$s），或参数用 + 拼接、replace 插入，或给 %s 传 number
- 读到：源端用 String.format(...)、SimpleDateFormat 或拼接生成带固定措辞的显示文本；写错的样子：目标 Text(...) 的实参是反引号模板或 + 拼接
适用范围：源端可见文案带格式参数，迁成 $r 或 resourceManager 取串时
做法：
- 找模板：有资源键的，到源工程各语言的 strings.xml 读 value；代码里格式化的取格式串，固定措辞原样留、变量换成占位，登记进目标 string.json
- 数出各占位的序号和类型，找到源端代入点逐个对上实参；由框架代入的，查清代入什么
- 写成 $r('app.string.键', 实参…)，非 UI 代码用 getStringSync(id, ...args)；%s 类占位的实参传 string，数值先 toString()
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- declare function $r(value: string, ...params: any[]): Resource：后面的参数依次替换字符串里的占位符；params 是 any[]，编译期不查和占位类型是否匹配（出处：鸿蒙 SDK 的 ets/component/common.d.ts，$r）
- value 里有 %1$s、%2$d 两个占位符时写 $r('app.string.label', 'aaa', 444)：多占位符的访问写法，参数按顺序替换（出处：resource-categories-and-access.md，访问本模块资源或模块依赖的HAR资源）
- 支持的占位：%d、%f、%s、%%、%数字$d、%数字$f、%数字$s：目标字符串资源里可以保留安卓的 %s、%1$s 写法（出处：js-apis-resource-manager.md，getStringSync<sup>10+</sup>）
- getStringSync(resId: number, ...args: Array<string | number>): string：非 UI 代码里按资源 ID 取格式化串，args 依次替换占位符（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，ResourceManager.getStringSync）
- getStringByNameSync(resName: string, ...args: Array<string | number>): string：同族接口：按资源名取格式化串（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，ResourceManager.getStringByNameSync）
- public final String getString(@StringRes int resId, Object... formatArgs)：源端 getString 第二个起的参数是格式化参数，对应目标的 args（出处：android.content.Context#getString）
针对本应用要查的：
- 模板的逐字值和占位符：源工程 res/values*/strings.xml 里该资源键的 <string name>；代码里格式化的，看给控件设文本的 Kotlin/Java 代码里 String.format 的格式串、SimpleDateFormat 的 pattern 或拼接表达式；固定措辞原样抄，记下每个占位的序号和 s / d 类型，各语言照搬到目标 resources/<限定词>/element/string.json 的同名条目
- 每个占位对应的实参：源端的代入点：getString / stringResource 第二个起的参数；不在调用点的，看框架在哪里代入；按占位序号对上实参。例：ListPreference 的 android:summary 含 %s 时，框架在 getSummary 里代入的是当前值在 android:entryValues 里的下标对应的 android:entries 项
未核实：%s 占位收到 number 时为空的行为，卡里观察自鸿蒙 SDK API 24（6.1.1），本机核实声明用 API 23
来源：3 张卡，3 个应用
- case-bcc79fa7d3d15ef4a8b2（jerboa）：做法第 3 步 ← 建议 4
- case-bdbb705b26462605b1c3（AntennaPod）：做法第 1 步 ← 建议 5；做法第 2 步 ← 建议 5
- case-c8f1e6989f066bb2f51a（掌上燃气管家）：做法第 1 步 ← 建议 1

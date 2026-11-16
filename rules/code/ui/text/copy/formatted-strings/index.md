# 带格式参数的文案

agent 会看到什么：源端 getString / stringResource 带实参、android:summary 的 %s，或代码里 String.format / SimpleDateFormat / 拼接出的文案，对应目标 $r('app.string.…', 参数…)、getStringSync(id, ...args)、模板字符串、+ 拼接和 replace 插入

## 通用查法

### 源端文案带格式参数时，读出资源模板的占位符和代入点，目标按序传参给 $r

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

## 规矩

- rule-d784bb79d864｜stringResource 带参数时映射成 $r('app.string.x', a, b)，不手工拼接｜读到：源端 Compose 用 stringResource(R.string.<键>, a, b) 套 %1$s / %2$s 模板；写错：目标把 ResourceStr 类型的参数直接 + ' ' + 拼接，没走资源模板：显示出对象字符串，模板里的固定词（如 ago）丢了
- rule-27854595112b｜字符串资源占位是 %s/%1$s 时，$r 的格式化参数传 string，数值先 toString()｜读到：stringResource(R.string.x, 数值) 传 Long/Int，对应字符串资源值里的占位是 %1$s；写错：$r('app.string.x', 数值变量) 直接把 number 传给 %s/%1$s 占位，界面上占位处为空
- rule-ae63aefa075f｜移植 getString 的 %1$s 位置参数时用 split/join 字面插入，不当 replace 替换串｜读到：`getString(R.string.…, name)` 或 String.format 带 %1$s 等位置参数，参数是用户数据；写错：目标格式化写成 s.replace('%1$s', arg)（或从兄弟页沿用的同类 helper），名称含 $$、$& 时被当作替换模式
- rule-6fa4d9019882｜源端在代码里格式化出带固定措辞的文案时，目标建参数化字符串资源，用 $r 传参｜读到：源端 Kotlin/Java 用 `SimpleDateFormat("yyyy年M月")`、`String.format(...)` 或字符串拼接生成带中文单位或固定措辞的显示文本，不在 strings.xml 里；写错：目标把这段文案写成模板字符串或 `+` 拼接直接传给 `Text(...)`，没有对应的 `$r('app.string.…')`
- rule-5f041b6fb987｜ListPreference 的 summary 串含 %s/%1$s 时，目标摘要要代入当前选项的显示文字｜读到：偏好 XML 里 ListPreference（或它的子类）带 android:summary="@string/…"，这个字符串的值里有 %s 或 %1$s；写错：目标摘要写成 $r('app.string.…') 不传参数，界面直接显示 %1$s；或者因为子类里没有 setSummary 就当成静态文字
- rule-6be1efef69d9｜克隆回调取编辑草稿和重排后的子项，名称用带占位符的字符串资源格式化原名｜读到：源端克隆：copy(id = 0, name = getString(R.string.…, 原名))，子项 mapIndexed 重排并清 id；确认克隆时传入草稿的 name、description 等字段；写错：目标 clone(id) 按 id 读已持久化的记录，以 { ...record, id: 0 } 原名插入，没有后缀，也丢了未保存的编辑

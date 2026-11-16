# 可见文案的逐字取值

agent 会看到什么：源端 strings.xml、R.string / Res.string、android:text 和偏好对话框给出的界面文案，对应目标 Text(...) 的字面量或 $r('app.string.…') 引用的是哪一条、值和源端是否逐字一致，以及空值时回退的占位文案

## 通用查法

### 可见文案先沿源端调用链找到资源键，再到 strings.xml 读逐字值，写成 $r 资源

审的是：代码
触发（任一种）：
- 读到：源端可见文案经 stringResource(R.string.…)、Res.string.xxx、getString 间接引用，或在代码里用 String.format 拼出；写错的样子：目标 Text(...) 里的文案是枚举名、路由名、@Preview 示例或自拟的字面量，和源端 strings.xml 的逐字值不同
适用范围：给目标页面、路由表和弹窗定可见文案时
做法：
- 从页面实际调用点找资源键：枚举 label、路由标题、stringResource(…) 的实参；只出现在 @Preview 或 docs 截图里的不算
- 按键名到源工程 strings.xml 找 `<string name="键">`，原样抄值（含括号、大小写、标点）；代码里拼出的取格式串，变量换成 %s
- 写进目标 string.json，页面用 $r('app.string.键', 参数…) 引用
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- declare function $r(value: string, ...params: any[]): Resource：取资源，后面的参数依次替换字符串里的占位符（出处：鸿蒙 SDK 的 ets/component/common.d.ts，$r）
- value 里有 %1$s、%2$d 两个占位符时写 $r('app.string.label', 'aaa', 444)：多占位符的访问写法，参数按顺序替换（出处：resource-categories-and-access.md，访问本模块资源或模块依赖的HAR资源）
- (content?: string | Resource, value?: TextOptions): TextAttribute：Text 的内容可以直接传 Resource（出处：鸿蒙 SDK 的 ets/component/text.d.ts，TextInterface）
针对本应用要查的：
- 每段可见文案的资源键：源工程里该区块调用链上的 stringResource(R.string.…)、Res.string.xxx、getString 调用；引用的是枚举或路由时，先在源码里找到它对应的资源键；对键名做全仓搜索，引用只出现在 @Preview 函数或 docs 下的不当作应用文案
- 资源键的逐字值：源工程的 strings.xml（Android 在 res/values/ 下，Compose Multiplatform 在 composeResources/values/ 下），按键名找 `<string name>`；原样抄 value，含括号、大小写和标点
来源：3 张卡，2 个应用
- case-55e8dd5a2281c1b13411（Meshtastic）：做法第 1 步 ← 建议 4
- case-6bfa66c963473bc7bea1（Meshtastic）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1
- case-c8f1e6989f066bb2f51a（掌上燃气管家）：做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 1

## 规矩

- rule-fe2f394c452b｜Tab 标签、页面标题、设置行等可见文案，沿源端资源引用链取 strings.xml 逐字值｜读到：源端可见文案经资源键间接引用：导航目的地枚举的 label = Res.string.xxx、路由的标题资源、顶部栏 title = stringResource(Res.string.xxx)；写错：Tab 标签、路由标题、设置入口行写成枚举名或路由名（如 Text('Map')、Text('Messages')）或自拟英文（'User Config'），和 strings.xml 的逐字值不同
- rule-1becedf3e1f8｜选空态等文案时以页面调用链为准，不取 docs 截图和 @Preview 的示例文案｜读到：仓库里有 docs/assets 截图和 @Preview 函数，里面的示例文案和页面调用链里 stringResource(R.string.…) 用的不一样；写错：目标的空态或提示文案取自截图或 @Preview 的示例字符串（应用代码里零引用），与已读到的调用点不一致
- rule-daafee8ee025｜源布局的页面专属文案在目标 string.json 里缺失时，用专属新 key，不拿通用资源顶替｜读到：源布局 XML 里 TextView 的 android:text 是硬编码的页面专属文案（如空态提示），目标 string.json 里没有对应条目；写错：目标写成 Text($r('app.string.…')) 引用一个语义相近的通用资源（如通用的「暂无数据」），文案与源不同
- rule-9350d3061e01｜弹窗专用文案在目标字符串表里缺时，按源端原文新建资源或留 HANDOFF，不借用别处文案｜读到：源端弹窗配置里的标题、说明、按钮文案在目标 string.json 里搜不到；写错：目标用其他页面的 $r('app.string.…')（如个人中心的同类条目）顶替标题正文，按钮用通用取消/确定冒充「同意并继续 / 不同意」；没有新增资源，HANDOFF 和 uncertain_regions 里都没提
- rule-4d1711992764｜偏好对话框没声明按钮文案时引用框架译文资源，不借应用同名的 ok、cancel、confirm｜读到：<ListPreference> / <EditTextPreference> 只有 entries、entryValues、key、title、dialogTitle，没有 android:positiveButtonText / android:negativeButtonText；写错：对应弹层的按钮写 $r('app.string.cancel')、$r('app.string.confirm') 这类应用字符串
- rule-744225556f07｜页面读回的字符串首尾带引号或反斜杠时，回资源层改 string.json，不在页面里剥｜读到：getStringSync 或 $r 读回的字符串值首尾带字面双引号，或残留反斜杠，源 strings.xml 里对应的 <string> 是用双引号包着或带转义的；写错：页面代码在 getStringSync(...) 的结果上再剥一层引号或去反斜杠（自写的取值辅助函数、.replace(...)、首尾截取）
- rule-020edc7b0800｜给既有 UI 模型展示字段填值时保留构建器的空值回退，不用状态描述或计数顶替标签｜读到：安卓列表项布局里该 TextView 的 android:text 是静态占位文案；目标构建器写 Text(item.field.length > 0 ? item.field : $r('app.string.…')) 这类空值回退；写错：数据映射把该字段填成另一条状态文案（如「暂无时间」）或计数 `${list.length}`，或把构建器改成 Text(item.field) 删掉回退
- rule-3f49565c7ca3｜源端登录分支调用带空值兜底的 getter 时，目标调用已移植的同名 getter，不读原始字段｜读到：源端刷新界面时 if (已登录) setText(管理器的 getter()) else setText(未登录占位)，getter 方法体里空值返回默认文案；写错：目标登录分支读原始字段写成 `字段.length > 0 ? 字段 : 未登录占位文案`，没调用已移植的同名 getter

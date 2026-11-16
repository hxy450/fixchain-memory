# DialogFragment 参数经 setter 注入时，规格写明重建后丢失哪些字段、内容和按钮变成什么

审的是：规格
触发（任一种）：
- 读到：所在 Activity 没声明 android:configChanges；DialogFragment 子类的监听器、文件路径、标题、预填文本经 setter 或构造参数写进实例字段，没有放进 setArguments，也没有在 onSaveInstanceState 里存；写错的样子：规格只写「托管 DialogFragment 保留」「目标不重建，弹层随页内状态保留，onConfigurationUpdate 不关闭」，没有逐个对话框列出重建后丢失的字段和按钮效果，也没有对应的验收条目
适用范围：源 Activity 未声明 configChanges、用 DialogFragment 承载弹窗时，规格里写配置变化或重建契约的那一节
做法：
- 逐个托管对话框列两栏：重建后保留的（setArguments 里的参数、对话框自己 onSaveInstanceState 存的、视图自存的状态如 EditText 已输入文字），重建后为空的（经 setter 或构造参数注入的监听器、文件路径、标题等）
- 写出重建后的内容与按钮效果并列为验收条目：托管对话框仍重显、目标不主动关闭，但内容按无参新实例（列表回到默认数据、无标题），依赖监听器的按钮只关闭、点行不回调
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Fragment 的子类必须有公开无参构造；状态恢复时框架用它重新实例化，带参构造不会被调用，参数只能经 setArguments 传入、getArguments 取回：重建后的 DialogFragment 是无参新实例，setter 写进字段的值不在（出处：android.app.Fragment 类注释与 Fragment#Fragment() 注释）
- EditText#getFreezesText 返回 true：EditText 的文字由视图自己存进状态，重建后保留（出处：android.widget.EditText#getFreezesText）
- 未声明 configChanges 时，转屏、换语言等配置变化会销毁当前 Activity，再用上一个实例的 savedInstanceState 新建一个实例：托管对话框随新 Activity 实例一起重建（出处：android.app.Activity 类注释「Configuration Changes」一节）
- 重建后的托管对话框：列表回默认数据、无标题、点行无效，按钮只关闭；EditText 文字保留：源端转屏后实测到的效果（出处：卡里修好并验证过）
针对本应用要查的：
- 每个 DialogFragment 哪些字段经 setter 注入、哪些放进了 arguments 或自存状态：源工程里这个 DialogFragment 子类的 Java 或 Kotlin 文件：setter 方法、newInstance/setArguments、onSaveInstanceState、onCreateDialog；onCreateDialog 和 onClick 里用到、却只由 setter 赋值的字段，重建后为空；按为空时代码走哪条分支写出重建后的内容和按钮效果
来源：1 张卡，1 个应用
- case-a95e51b69844d2f11187（Sokoban）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1、建议 3；取值 4 ← 诊断

# 给 android:label 写验收条目时只写键名或照抄 strings.xml 的值，不补未读到的字面值

审的是：规格
触发（任一种）：
- 读到：源 Manifest 的 android:label="@string/app_name"，只给出资源键名，值要到 res/values*/strings.xml 查；写错的样子：验收条目写成「app=@string/app_name（"某个名字"）」，括号里的字面值没有出处、和 strings.xml 不符；真值锚点指向 Manifest，没有决策锚点
适用范围：规格提取阶段为 Manifest 里引用资源的属性（应用名、标签）写验收条目时
做法：
- 验收条目只写键名（app=@string/app_name），或先打开 res/values*/strings.xml，把各语言的实际值照抄进去
- 确需与源值不同，在决策台账登记决策 ID，条目写「决:」锚点和 decision_ref
针对本应用要查的：
- 资源键的实际值：源工程 res/values*/strings.xml 里同名的 <string>，以及模块构建脚本里的 resValue；逐个语言目录读出，写进验收条目；读不到就只写键名
来源：1 张卡，1 个应用
- case-9e50f3aa8db41be6d2fe（Privacy Friendly 2048）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 1

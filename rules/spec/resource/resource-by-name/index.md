# 按资源名引用的颜色和尺寸资源

agent 会看到什么：读过的源码用 getColor(R.color.名) / getDimension(R.dimen.名) 按资源 ID 取值，工程里另有名字含同一颜色词的近名 <color> 资源；交回的规格里色表、常量表或验收把近名资源合成一行、标错 hex，或只写颜色词

## 规矩

- rule-ef0837dc49f3｜源码用 getColor(R.color.名) 等取资源值时，规格按精确资源名查定义写值，不按颜色词近似｜读到：安卓源码按资源 ID 取值：getResources().getColor(R.color.名)、getColor(R.color.名)、getDimension(R.dimen.名)；工程里另有名字含同一颜色词的近名资源；写错：验收条目、算法说明或常量表里写成「R.color.名(#hex)」，而这个 hex 在 res/values*/ 里属于另一个 name 的资源；或者只写颜色词，不写定义所在的文件和值
- rule-d12eb1774d35｜工程里有几个含同一颜色词的颜色资源时，规格色表按资源名逐行列，不合并近名资源｜读到：源工程 res/values*/ 的 XML 里有几个名字含同一颜色词的 <color> 资源（如一个不带前缀、一个带用途前缀），分别被不同的方法或绘制项通过 R.color.名 引用；写错：规格色表把近名资源合成一行，或两行标成同一个 hex；某一行只写颜色词，缺资源名、定义文件或消费点

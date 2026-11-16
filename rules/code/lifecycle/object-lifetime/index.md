# 源端对象、静态字段和监听的存活期

agent 会看到什么：读到源 Activity 的实例字段存会话数据、类的 static 字段、getLastNonConfigurationInstance 判空分支、Fragment 只注册不注销的监听；产物里服务的 getInstance() 单例、静态引擎的每局复位函数、hasInstance() 分支、aboutToDisappear 里补的注销

## 规矩

- rule-2bac63bc95ca｜服务持有 Activity 实例会话态时，页面 new 一个服务实例，不用 getInstance() 单例｜读到：源 Activity 的实例字段存会话数据，服务逻辑直接读写这些字段；写错：页面从服务类的 getInstance() 取单例，把 Activity 字段搬进单例，靠 attach / reset 复位近似实例重建
- rule-0d7a305ee375｜多个源对象并进静态引擎时，复位函数的每条赋值都要对得上源端每局路径里的赋值｜读到：源端类的 `static` 字段、宿主 View / Activity 的实例字段，在每局重开函数和其中 new 出的对象构造里都没有赋值；写错：目标模块级静态引擎的每局复位函数里给这类字段重新赋初值（把计数设回常量、把 boolean 标记设回 `false`），源端每局路径里找不到对应赋值
- rule-baa4e42b9e39｜源端按 getLast…NonConfigurationInstance 判空分支时，目标按配置重建标志分支｜读到：Activity.onCreate 里 getLastCustomNonConfigurationInstance() / getLastNonConfigurationInstance() 为 null 才按 Intent 启动参数分支；写错：目标代码写成 if (!…hasInstance()) {按启动参数分支} else {复用单例}，或用全局状态是否存在决定是否忽略启动参数，注释写「续存优先：参数忽略」
- rule-f105f83e371a｜源端只注册不注销的监听，迁移时先查目标壳层的真实存活期，不机械补「离页注销」｜读到：源端 Fragment 只注册监听，没有对应的注销调用（onDestroyView、onDestroy 里都没有）；写错：目标页面在 aboutToDisappear 里补了源端没有的注销，而主壳用 if (currentTab === n) 条件渲染这个页面，切 Tab 就销毁

# SharedPreferences / DataStore 的偏好键和默认值

agent 会看到什么：读到 DataStore getter 写成 preferences[KEY] == true 或带 ?: 默认值、Compose 里对 collectAsState 收集的状态判 == null、键表里同类数据分成几组独立键、全局键值工具要先 init(context)；规格的偏好表、触发条件、AC 写成三态 null、「首次进入」、合并的两组持久化或只写「已实现」

## 规矩

- rule-d216933bd2f9｜偏好默认值按 DataStore getter 的映射写，不从一个 null 判断推出三态偏好键｜读到：DataStore getter 写成 preferences[KEY] == true（或 ?: 默认值），返回非空 Boolean；写错：偏好表把该键默认值写成「null（未初始化，区分首启）」，或同一份规格里既写「Boolean 默认 false」又写「== null 表示未写入」，契约里出现 boolean | null 的参数
- rule-8436f7b0eeeb｜源端对非空状态做 == null 判断时，规格记成永不触发的死分支，不译成首启或未初始化｜读到：Compose 显示条件里对状态变量写 == null / != null，而该变量由 collectAsState(initial = false) 收集，Flow 的 getter 映射成 preferences[KEY] == true 或带 ?: 默认值；写错：规格把这个条件写成「首次进入」「设置未初始化（…== null）」时触发弹窗或权限请求
- rule-1ee735014122｜源端同类偏好拆成多组独立集合时，AC 按写入它的页面分到各功能，括注不超出本行源锚点｜读到：源端偏好仓库的键表里同类数据有几个独立键（按来源、目标等分组），各由不同页面或 ViewModel 写入；术语表写明某一组归另一个页面；写错：某功能的 AC 写成「…持久化（A/B 两组）」，而同一行的源锚点只列了其中一组的字段或方法，目标方法也只对应这一组
- rule-5f121bd93e94｜基础层规格写明偏好存储封装须先 init(context)、在哪个生命周期 init｜读到：源端全局静态键值工具保存 token、用户信息，原生页面和 MethodChannel 回调都读写它；写错：基础层规格只写偏好存储封装「已实现」和键对齐表，没写必须先 init(context)、init 放在哪个生命周期、启动期有哪些读写方
- rule-8ac081bc8000｜源端同步读设置、目标端改异步时，源码笔记写异常分支、差异记进 Spec Gap List｜读到：安卓源端在首帧前用 SharedPreferences.getString / getInt 带默认值同步读设置，界面没有加载态和失败态；目标端的偏好读取是 async；写错：source-notes 的 presenter 摘要没有“异常分支”一项；Spec Gap List 没记“源端同步读取、目标端异步且可能失败”这一差异
- rule-76b649c3130c｜源码里 putString 被注释、改调会话 setter 的设置项，规格登记为会话态，不列进偏好键｜读到：源端设置弹窗里写 SharedPreferences 的 editor.putString(...) 被注释掉，旁边改调应用接口上的 setter（只改会话字段），读取处同样是 getString 被注释、改调 getter；写错：规格把这个设置项列进「读写偏好键」清单，验收条目写成「切换写 <偏好键>」，或注「语义见某权威表」而那张表里没有这一项

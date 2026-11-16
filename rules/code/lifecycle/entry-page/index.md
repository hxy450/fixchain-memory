# EntryAbility 的入口页和启动顺序

agent 会看到什么：目标工程 EntryAbility 的 onCreate / onWindowStageCreate、loadContent 加载的入口页（DevEco 模板的 Index）、main_pages 登记和 @Entry / export struct，以及首屏前的异步装配

## 规矩

- rule-86cd125d76f7｜模板工程的入口页要覆盖为主界面时，交回前读回核对已不是 Hello World 模板｜读到：目标工程 EntryAbility 的 onWindowStageCreate 里 windowStage.loadContent('pages/Index')，Index.ets 是 DevEco 模板（struct Index、@State message: string = 'Hello World'）；写错：交回时入口页仍含 'Hello World' 和 RelativeContainer 或 Row/Column 模板结构，没有计划的根组件（如 Tabs 和 TabContent）
- rule-756a30b17c65｜报 10905402 或 @Entry 与 export 同在时，先判定页面角色再改登记或装饰器｜读到：编译错误 10905402：main_pages 登记的页面须有且仅有一个 @Entry；写错：给被 Tabs 或父页面 import 的子组件补 @Entry 并保留 export struct
- rule-b3de600f4346｜页面从异步装配的服务槽位取依赖时，提供可等待、失败可复位的幂等就绪门，首屏 await 后再路由｜读到：EntryAbility.onCreate 以 void 方式调用异步装配（不等待），随后 onWindowStageCreate 里 loadContent 加载入口页；写错：首屏在 onReady 里同步读可空槽位，读到 null 只记一条日志就 return，沿用默认路由；或只有 Ability 私有的 Promise，首屏没法等
- rule-620aa036bbea｜异步装配时先发布路由所需的服务，数据库等慢初始化放在其后｜写错：装配函数先 await 数据库 init(...) 再写入启动、鉴权、网络这类路由所需服务的槽位

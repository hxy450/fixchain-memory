# SharedPreferences 迁成 preferences 的偏好存储

agent 会看到什么：源端 SharedPreferences / MMKV 的读写、Editor 累积后 commit、Application.onCreate 里按标记门控的初始化、存进偏好的 bean，对应目标 preferences 封装的 init 位置、putSync / flush 和存进去的 JSON

## 规矩

- rule-3f9fe9393e4f｜应用级偏好存储封装在 UIAbility.onCreate 初始化，不只挂在 Flutter 插件 attach 上｜读到：源端 MethodChannel 回调里直接读写全局静态键值工具（MMKV 或 SharedPreferences 工具类的 getString / putString），通道本身不初始化存储；写错：偏好存储封装的唯一 init(context) 在 Flutter 插件的 onAttachedToEngine 里（用 binding.getApplicationContext()），EntryAbility 的 onCreate 里没有 init
- rule-2ab6f4a652f5｜需先 init 的存储封装未初始化就读写时打错误日志，不静默返回默认值｜写错：封装里 context 或 preferences 实例为空时 getString 直接返回默认值、putString 直接 return，没有任何日志
- rule-aa7964769786｜迁移 Application.onCreate 里的首次启动初始化时，在目标启动路径落实际调用并保留门控｜读到：源端 Application.onCreate 调用一个首次启动初始化方法，方法里按 SharedPreferences 标记（或空库判断）门控，只在未执行过时写入数据；写错：目标的数据管理器构造只加载已有数据，初始化函数只由设置页的重置入口调用；EntryAbility.onCreate 和数据管理器初始化里都没调用它
- rule-bacedc6590b0｜源端 Editor 累积后一次 commit 的恢复流程，目标先暂存、全部通过后再 putSync｜读到：恢复时往 SharedPreferences.Editor 里逐键 put，末尾一次 commit()，中途异常直接返回 false；写错：目标在解析过程中逐键 putSync 写进共享 Preferences 实例，最后才 flushSync；中途失败时已解析的值留在实例里
- rule-b1f521fa18bb｜迁移设置页的保存逻辑时，源端保存的每个副作用都要在目标落地，只写远端设置不算完成｜读到：源设置页的保存处理除远端保存外，还调用本地配置更新方法，并发同步或刷新事件（如 EventBus.post、sendBroadcast）；写错：目标的保存函数里只有写远端设置 JSON 的调用，没有本地配置写入，也没有 emitter.emit 之类通知读取它的列表刷新的调用
- rule-f9d8120d1722｜模型带 bigint 字段时，每条 JSON 持久化往返都配成对的 replacer / reviver｜读到：源端被存进偏好或数据库的 bean 有 Long 字段；写错：存取用户等对象时用裸 JSON.stringify(obj) 存、JSON.parse(json) 取，DAO 或 preferences 里存的 JSON 也没处理 bigint
- rule-bd6652b1ad39｜源端偏好同步构建时，封装用 getPreferencesSync 和 *Sync 提交，不做异步载入加写队列｜读到：源 SharedPreferences 在 Application.onCreate 同步构建，此后各处直接 getBoolean / getString 读；写错：封装用 preferences.getPreferences(...) 异步载入加内存缓存和 pending 写队列，注释写「读取前不阻塞」，就绪前读返回调用方默认值，put / delete / clear 各自异步排队
- rule-1b97551106a2｜关闭某模式时要求移除偏好键的，目标用 deleteSync，不写成 putSync(键, false)｜读到：规格或源码写明关闭某模式时移除该键（SharedPreferences.Editor.remove）；写错：目标关闭分支写 putSync(<键>, false)，键仍然存在
- rule-972b6f2239eb｜偏好值的序列化格式以源函数和同工程其他读写方为准，读写两端用同一格式｜读到：源端读写某个偏好（如分辨率）的函数用 SharedPreferences 存成特定分隔的字符串，同工程别的页面也读写同一个键；写错：目标端 getter 按另一种分隔拆分、setter 写 `${width}x${height}`，和源格式或同工程其他读写方不一致；契约要求的参数被去掉

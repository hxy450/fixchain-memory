# 构建配置决定的实现和接口环境（BuildConfig 开关、多套 base URL）

agent 会看到什么：读到源码按 BuildConfig 布尔开关在新旧两套实现间择一启动，或 API 清单的 base_urls 只给地址常量的键名；规格写「两路径取并集」、验收照停用实现写，或只列一个 Base URL、写没有出处的 dev/staging/prod

## 规矩

- rule-69a96861c082｜构建开关在新旧两套实现间二选一时，规格先查开关取值，以启用的一套为行为基准，不取并集｜读到：源码按 BuildConfig 布尔开关在两套实现间择一启动（如 starter 里 if (BuildConfig.USE_…) 选服务），停用的一套在开关为真时于 onCreate 抛 IllegalStateException；写错：规格基线写「两路径的行为断言取并集」，冲突路径的验收条目照停用实现写（如换集时收尾上一集、跳过即标记已播、只在某一状态回退）
- rule-8083e8d912f8｜API 清单只给地址键名时，规格回源码写出各套接口各环境的 host、环境枚举和默认环境｜读到：API 清单的 base_urls 只给出地址常量的键名（指向源文件里的常量），没有任何 host 和环境取值；写错：规格写「BASE_URL（…配置，多环境 dev/staging/prod）」这类没有出处的环境词表，只列一个 Base URL；源端分新旧两套接口时漏掉另一套地址
- rule-b1050cfa0142｜同一功能有新旧两套源实现时，规格的 races / 生命周期规则标明适用页面｜读到：同一功能有两套源 Activity：旧版在 surfaceCreated 里按「面已创建 ∧ 正在播放」双守卫挂面，新版在 MediaController 就绪后直接 setPlayer；写错：规格 races 节或验收条目把一套实现的守卫（如「videoSurfaceCreated ∧ status==PLAYING 双 guard」）写成通用规则，没限定适用页面
- rule-849d9168ab2d｜资源映射文档的 flavor 来源照台账指定的写，不自定默认 flavor｜读到：源工程有多个 productFlavors，各 flavor 自带 app_name / app_package；决策台账或派工写了默认 flavor；写错：资源映射文档里身份串一节写成另一个 flavor 的值和 flavor 源（如「play flavor app_name=…，flavor 源 src/play」），或转换脚本注释写「play = default flavor」、默认取第一个 flavor
- rule-af0c4e7657da｜源端功能在参照构建里不触发时，规格按不触发落地，不新增同意门控和本地采集链｜读到：源端初始化被构建期配置短路：`if (!TextUtils.isEmpty(BuildConfig.…))` 包住 ACRA.init，参照构建里该值为空，上报静默禁用；写错：规格或台账为「平台合规」新增隐私同意门控、本地崩溃日志采集链，把源端的启用开关默认值改成关，并标 HARD-DIV

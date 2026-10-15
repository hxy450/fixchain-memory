# ui/state

ArkUI V2 状态刷新与订阅：@Builder 参数（含异步重赋值的数组与对象）、复用开关组件的事件值、页面与共享模型的绑定、共享状态 key 的命名、按状态显隐、只在回调执行后才成立的显示状态与控件自带的前置过滤、负责上抛自身可见性的组件须常建、事件驱动的重新加载、生命周期回调迁入 ViewModel 时的成对状态、单例 ViewModel 的取消语义与页面加载入口单飞、ForEach 键与子组件刷新、变更信号与 @Monitor 数组路径的配套、可观察字段的判定、监听的注册与释放、乐观更新与访问器兜底，多个 ViewModel 实例间的跨页面状态（拆单例、弹窗与宿主），稳定列表键与可观察实例原位更新，Repeat 条目的传参，离开组合即销毁的复位与框架会恢复的界面状态，Activity 实例会话态的作用域，每次可见时的初始化与只在可见时接收的监听；Compose remember 的求值与重建时机（无键、带 key、条件挂载、无 key 惰性项），以引用比较实现的未保存检测

[上一级](../index.md)

## 本级经验

- [AppStorageV2/PersistenceV2 的 key 只用字母、数字和下划线，不沿用 kebab-case 文件名](lesson-7508ddc52eaf816887f0.lesson.md)
  - 时机：状态管理实现阶段，为 AppStorageV2.connect 或 PersistenceV2 共享状态类确定 key 字符串，或复用工程已有 key 时
  - 情境：ArkTS V2 工程以 AppStorageV2.connect(Cls, key, creator) 跨页面共享 @ObservedV2 状态；模块文件名采用 kebab-case（如 window-model.ets），状态管理 skill 只给出签名和一致性示例；编译期不校验 key 内容。
- [SearchView.onQueryTextSubmit 等回调里才置位的尾部按钮与进度，连同触发时机和控件自带的空提交过滤一起移植](lesson-af89611fa71ea0eb6f45.lesson.md)
  - 时机：界面实现阶段，把 Android 回调中的命令式状态（尾部按钮、进度、空态）和控件监听映射为 ArkUI 声明式条件与事件时
  - 情境：源在 onQueryTextSubmit 等回调触发的搜索流程里才设置尾部按钮与进度条；SearchView 只在去空白后非空时回调 onQueryTextSubmit，映射参考只给出监听名到事件名的对应，不含这层过滤。
- [列表条目以同键新对象替换或整表重建时，按渲染器确定新值怎样到达条目：键并入可变字段，或改为可观察实例原位更新](lesson-2e636699fa65aefd63f0.lesson.md)
  - 时机：功能实现与页面接线阶段，为可编辑或会重新拉取的列表选定条目更新方式与 ForEach 键时；为消除重建抖动而稳定 ForEach/Repeat 的键时
  - 情境：列表条目编辑后以保留 id 的新对象替换（copy、arr\[pos\] = 新实例、splice），或操作成功后重新请求并整表赋值（id 不变、计数等字段变化）；目标用 ForEach 或 Repeat 渲染，键只含 id 等不变字段，条目字段作为子组件 @Param 传入。源端是 Compose 不设 key 的 forEach 加不可变 copy，或 RecyclerView 整表刷新、remove+add+notifyItemChanged。也包括为消除重建抖动把键缩成只含页标识而页模型仍是普通对象，以及只由显示内容拼出的键（内容可能完全相同）。
  - 例外：更新方式是对 @ObservedV2 条目的 @Trace 字段原地赋值，子组件绑定的仍是同一对象，此时可保留只含 id 的键；Repeat 开了 virtualScroll：同键新对象会经 updateItem 送进 RepeatItem，builder 直接读 ri.item 即可，保持稳定键
- [判定模型字段不需要可观察之前，先读修改它的方法和显示它的界面](lesson-4d1c980bbbd20275f5c3.lesson.md)
  - 时机：数据模型阶段，决定模型字段是否需要 @Trace 或其他可观察包装，或在模型注释里写“静态、不会修改”时
  - 情境：源端模型是不可变数据类，字段值通过 copy 替换变化；只读模型定义看不出哪些字段会变，目标端要决定哪些字段可观察。
- [复用开关组件的变更事件给出目标值时，把它原样写入该开关的 setter，不改成无参回调再按旧值取反](lesson-40fc63b124b4a44e7a9f.lesson.md)
  - 时机：界面接线阶段，把开关行接入带 @Param isOn 与 @Event onToggleChange(nextState) 的复用组件，并连到 ViewModel 的开关接口时
  - 情境：源端每个开关点击时翻转自身字段、写偏好并刷新自身图标；目标复用组件在事件里给出下一状态，ViewModel 提供 toggleX() 取反接口，页面本地 @Local 与 ViewModel 各持一份开关值。
- [多个加载入口接到共享单例 ViewModel 时，同参数请求先单飞复用，需要只认最新请求时再按请求代次判旧，不写成新请求取消旧请求](lesson-c883a0ff96c32dfbd9ba.lesson.md)
  - 时机：页面接线阶段，把 aboutToAppear、Refresh 的 onRefreshing、@Monitor 等多个加载入口接到共享单例 ViewModel 或 Service 时
  - 情境：目标 ViewModel 为单例，run() 对任何新请求先取消上一请求；页面同时存在 aboutToAppear、Refresh（refreshing 初值可能为 true）与切换城市等业务键的监听等入口；源端 ViewModel 可能每次启动一组请求、不取消前一组；规格可能要求按业务键丢弃迟到响应、一次刷新只产生一次请求。
- [把源界面的生命周期回调迁入 ViewModel 刷新方法时逐条迁移全部赋值，成对状态的打开与关闭路径都要落地](lesson-d7c148c4a233c59ff151.lesson.md)
  - 时机：功能实现阶段，把 Compose 界面中的局部状态与 ON_RESUME 等生命周期回调迁入 ViewModel 方法、由页面 onShown/onPageShow 调用时
  - 情境：源界面用 remember 局部状态控制插页、弹窗等显隐，在 ON_RESUME 观察者里重查权限或数据，并按结果同时更新多个状态（如权限新获得时隐藏权限插页）；目标把这些状态集中到 ViewModel。
- [拆除共享 ViewModel 单例或让弹窗与宿主各持实例时，跨页面状态显式传递或从持久化重读，不只把 getInstance() 换成 new](lesson-fc724027e2c995632733.lesson.md)
  - 时机：架构重构阶段把跨页面共享的 ViewModel 单例改为页面级实例时；修复阶段为页面补传筛选参数，或让弹窗与宿主页各自持有 ViewModel 实例时
  - 情境：多个页面经全局单例（如 AppStorageV2）共用一个 ViewModel，其中的筛选或显示状态（当前空间、选中日期、显示偏好）由某个页面的动作写入，其他页面的查询只隐式读这份状态；重构要求改为页面级实例，或弹窗内改动的持久化偏好只经回调通知宿主，宿主刷新时又用自己实例的快照回填。
  - 例外：要解决的是同一实例内并发加载的迟到响应与重复刷新：按请求键丢弃旧响应、合并加载入口，不属本条
- [收藏、点赞类切换：规格写“点击即翻转”而源端在成功回调里才置状态时，按批准的契约决定先翻转还是回调门控](lesson-18c8e7630a96d66540bc.lesson.md)
  - 时机：界面交互实现阶段，编写收藏、点赞类切换的点击处理，确定本地状态翻转与服务端调用的先后时
  - 情境：验收要求点击后状态翻转、界面即时刷新（乐观更新）；源端把选中态设置写在网络接口的成功回调里；目标用状态变量驱动图标并异步调用接口。
  - 例外：规格与源码都把状态设置放在成功回调里：按源端回调门控，不引入乐观更新
- [源端 Activity 实例字段承载的会话态映射为页面实例作用域，只有源端本就静态全局的状态才做单例](lesson-d9143de006714935afe2.lesson.md)
  - 时机：规格提取与服务实现阶段，为页面编排服务确定作用域（单例还是页面实例），并迁移源 Activity 的实例字段（待写数据、密钥映射、挂起状态）时
  - 情境：源 Activity 把本次会话的数据（待写数据、密钥映射、挂起状态）放在非 static 实例字段里，没有经 onSaveInstanceState、ViewModel 或外部共享对象恢复；目标规格把页面编排服务写成单例，实现者用 getInstance() 持有这些字段，并以 attach 时复位来近似实例重建。
  - 例外：源端该状态本就是静态全局的（如公共类的静态字段），此时可以映射为单例；字段由 savedInstanceState、ViewModel 或外部注入的共享对象恢复或持有：按该来源的生命周期映射，不当作每次全新；状态在源端就由多个页面共享读写：作用域定下后，跨页字段按显式传参、订阅或持久化重读处理
- [源端以引用比较判断“有未保存改动”时，ArkUI V2 改用显式改动标志，不拿 @Local 数组与原数组或新字面量做 ===](lesson-5d6e099ff0c8965f2b3c.lesson.md)
  - 时机：界面实现阶段，把编辑页的未保存检测（离开前确认、canSafelyExit 一类）从 Compose 翻译到 ArkUI V2 状态时
  - 情境：源端编辑页以 remember(x){ mutableStateOf(x) } 一类写法让编辑状态的初值就是入参对象，修改时整体替换成新列表，再用 !== / === 引用比较判断是否改动；目标用 @Local 数组承载编辑状态，另存一份初始数组，或在新增模式把两者各自初始化为 \[\]。
- [源端显示值经带兜底的访问器或码值映射函数取得时，目标调用已移植的同一函数，不改读原始字段、不透传 code、不自拟兜底](lesson-1fa08bf929cfced0ff34.lesson.md)
  - 时机：功能接线阶段，把源端刷新函数里的显示赋值（如 text = Manager.getX()、text = Util.codeToText(code)）翻译成目标组件状态，或把登录判定与显示字段映射成文案表达式时
  - 情境：源端在某一分支调用带空值兜底的访问器（例：已登录但昵称为空时返回“用户{id}”或默认昵称），另一分支才显示“未登录”等占位文案；或经工具类把数值码映射为显示文案（天气码、等级、方向等）。目标侧会话或仓库层保留原始字段，可能已移植同名兜底方法或映射函数，组件状态是普通字段，工程里有现成的占位字符串资源。
  - 例外：整条记录映射成多字段 UI 模型（图标与颜色成对下传、构建器回退）：按适配层逐字段赋值的经验处理
- [源页面在 onResume、事件订阅或结果回调里重新加载数据时，按目标挂载类型接可见性回调或订阅，不只在 aboutToAppear 加载](lesson-b3bb0bc33f4caded78a2.lesson.md)
  - 时机：ViewModel 与页面接线阶段，决定目标页由哪些入口触发数据重新加载时；从常驻页新增 push 子流程时；把 Activity 的 onStart/onResume 初始化映射到目标页面回调时
  - 情境：源 Fragment/Activity 用 EventBus @Subscribe（登录成功、记录变化等）、ActivityResult 回调或 onStart/onResume 重拉数据、重读 Intent、重建列表；目标页是 Navigation 下常驻的根内容、Tab 页、NavDestination，或经 router.pushUrl 打开新增/编辑页后 router.back 返回的 @Entry 页，数据只在 aboutToAppear 或一次性的 onReady 拉取；工程可能已有会话状态与应用事件总线。
  - 例外：源端只在 onCreate 加载一次，没有可见性、事件或结果回调触发的重载：保持一次性加载；只在页面可见期才应接收的监听（硬件、标签）属于注册与注销的作用域决策，按可见期在 onShown/onHidden 成对处理，不在本条的重载清单里展开
- [用 @Monitor 监听数组路径代替 collect 时，生产方按源端以新数组重新赋值发出变更](lesson-0cc7ae4eec0a59086202.lesson.md)
  - 时机：状态模型与 ViewModel 实现阶段，把 StateFlow/Flow 的列表或消息队列迁成 @Trace 数组，并由消费方用 @Monitor 监听数组属性路径时
  - 情境：源端以 StateFlow.update { list + item } 一类写法每次发射新列表；目标生产方准备原位 push（出队却重新赋值），消费方以 @Monitor('model.items') 一类路径模拟 collect。
- [负责上抛自身可见性的组件必须常建：不用 if 包住它，隐藏态用零高加 clip 或 opacity，不依赖 Visibility.None 保证创建](lesson-3a00fd66c5188f5cfdf4.lesson.md)
  - 时机：界面实现阶段，翻译“容器初始隐藏、内部组件常驻并自行通知宿主显示”的结构，或向他人预留的条件槽位嵌入组件时
  - 情境：源容器 visibility=gone，但内部 Fragment 在 onCreate 即挂载，并由它调用宿主的可见性方法；目标用 if 或 Visibility 控制容器，或把该组件填进由宿主条件包住的槽位。
  - 例外：该组件不负责上抛可见性，由宿主或其他常建组件决定显隐：按宿主状态用 if 条件构建即可
- [迁移 Compose remember 一类局部状态时，按源端的求值与重建时机落实，不写成每次重算，也不让常驻组件跳过复位](lesson-3b4a96141329db62a6af.lesson.md)
  - 时机：界面实现或公共组件抽取阶段，把 Compose 中 remember、derivedStateOf、LaunchedEffect 持有或算出的局部状态迁到 ArkUI（写成 @Computed、getter 或缓存字段，提升为页级 @Local，放进常驻的 ListItem 或子组件，或改成选择 handler 里的直接赋值），并决定何时求值、何时复位时
  - 情境：源端状态写在无键 remember { … } 或 remember { derivedStateOf { … } } 包住的一次性判定（如按目标值是否含小数点决定是否显示小数）、remember(k1, k2){…} 派生值、条件挂载（if (show) Dialog/卡片）子组件内的 remember 与 LaunchedEffect，或 LazyColumn 中不设 key 的 item{}/items 项里；源码没有显式重算或清空，时机依赖组合身份。目标准备写成每次渲染都重算的 @Computed、getter，或把状态放到页级 @Local、常驻组件，或在每次点击时重写派生值。
  - 例外：目标保持与源端相同的挂载结构（条件渲染的子组件自己持有状态、每次显示新建实例），重建语义已自然保留；目标页保活、返回时由框架恢复的焦点或输入法改写已复位状态：按 TextInput 获焦来源判别处理，不属本条
- [迁移按状态切换的显示时同时迁移 setVisibility 分支：该状态下隐藏的控件不渲染，显示的区块要实现](lesson-43a9050245b1afa165bf.lesson.md)
  - 时机：界面实现与巡检修复阶段，迁移登录态等状态下控件的显示内容与显隐时；把 ViewHolder.bind 中的 setVisibility 逻辑移植到共享行组件时
  - 情境：源端 Fragment 或 ViewHolder.bind 按登录态、远端配置、播放状态等对多个控件 setVisibility（如登录后隐藏用户名、显示签到区），部分 setText 被注释；目标 ArkTS 按状态条件渲染；工程可能有显隐或绑定检查器报告源控件丢失。
  - 例外：节点在源 XML 中 gone 且代码从不设为可见（与状态无关）时，按静态可见性的规则不生成
- [随状态变化的控件参数不作 @Builder 位置值参，改为内联读取、@ComponentV2 子组件 @Param 或按引用传参](lesson-8d2979542fa2cd65150c.lesson.md)
  - 时机：界面实现阶段（页面转换与公共组件抽取），以及返修或按源端几何重写已有页面时，为源端带状态参数的子控件、多个同构开关行或数据文字选择 ArkUI 复用写法时；把 LazyForEach 改写为 Repeat、拆出条目 @Builder 时
  - 情境：源端 Compose 子 Composable 以当前状态算出的值作参数（如 enabled = count &gt; 1、颜色随选中态变化），或 Android 页面有多个同构的开关行、各自持有状态；目标准备把子控件或开关行抽成共享的 @Builder 方法，并把 this.&lt;状态&gt;、异步重新赋值的数组或对象（搜索结果、定位卡）、随布局或旋转变化的尺寸作为位置值参传入。也包括把 LazyForEach 改为 Repeat 时 each 回调写成 this.Row(ri.item)；以及为子页面嵌入点写只含前向引用的空 @Builder 槽位，参数表成为后续填充者的接口。
  - 例外：传入 @Builder 的只有文案、尺寸等在该组件生命周期内不随状态变化的值
- [页面向单例仓库或偏好注册监听时，把回调或句柄存成字段，在 aboutToDisappear 用同一引用移除](lesson-14b7f4090b7b83873b22.lesson.md)
  - 时机：功能接线阶段，在页面 aboutToAppear 里向应用级单例仓库、数据库或偏好注册数据监听时
  - 情境：目标数据层是应用级单例，用 addListener/removeListener（按回调引用移除）提供可观察数据；源端页面用 observeAsState、collectAsState 这类随界面生命周期自动结束的观察；ArkTS 子页出栈时不会自动注销。
  - 例外：只在页面可见时才应接收的监听（如 NFC 标签这类前台硬件事件）按可见期在 NavDestination 的 onShown 登记、onHidden 注销；按组件存活期注册时，被覆盖的页面仍会继续接收
- [页面直接读共享 @ObservedV2 模型的 @Trace 字段，不复制成 @Local 快照再手动同步](lesson-08c38f950b69e991607d.lesson.md)
  - 时机：功能接线与页面实现阶段，把页面显示状态接到 @ObservedV2 模型或共享 store，且模型会被其他页面、异步加载或服务回调改写时
  - 情境：目标端用 @ObservedV2 + @Trace 模型（AppStorageV2.connect 或单例 getter 取得）承载共享状态：源端由一个根状态持有者驱动多个屏幕，拆成 Navigation 下多个页面后由子页修改模型；或源端 Flow/StateFlow 持续推送列表与加载态，目标由异步加载、BLE/消息回调整体重新赋值 store 的 @Trace 字段，页面是 @ComponentV2 子组件。
  - 例外：需要与模型解耦的纯界面态（弹窗开关、未提交的输入草稿）仍放在页面 @Local；要解决的是返回时重新拉取数据（模型本身没有被更新）：按页面可见性回调或订阅重新加载，不属本条

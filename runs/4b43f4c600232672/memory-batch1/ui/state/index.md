# ui/state

ArkUI V2 状态刷新与订阅：@Builder 参数（含异步重赋值的数组与对象）、复用开关组件的事件值、页面与共享模型的绑定、共享状态 key 的命名、按状态显隐、事件驱动的重新加载、单例 ViewModel 的取消语义与页面加载入口单飞、ForEach 键与子组件刷新、监听的注册与释放、乐观更新与访问器兜底

[上一级](../index.md)

## 本级经验

- [AppStorageV2/PersistenceV2 的 key 只用字母、数字和下划线，不沿用 kebab-case 文件名](lesson-7508ddc52eaf816887f0.lesson.md)
  - 时机：状态管理实现阶段，为 AppStorageV2.connect 或 PersistenceV2 共享状态类确定 key 字符串，或复用工程已有 key 时
  - 情境：ArkTS V2 工程以 AppStorageV2.connect(Cls, key, creator) 跨页面共享 @ObservedV2 状态；模块文件名采用 kebab-case（如 window-model.ets），状态管理 skill 只给出签名和一致性示例；编译期不校验 key 内容。
- [共享单例 ViewModel 按规格的键丢弃过期响应，页面各加载入口先做单飞，不写成“新请求取消上一请求”](lesson-c883a0ff96c32dfbd9ba.lesson.md)
  - 时机：页面接线阶段，把 aboutToAppear、Refresh 的 onRefreshing、@Monitor 等多个加载入口接到共享单例 ViewModel 或 Service 时
  - 情境：目标 ViewModel 为单例，run() 对任何新请求先取消上一请求；页面同时存在 aboutToAppear、Refresh（refreshing 初值可能为 true）与切城监听等入口；规格要求按 areaId 一类键丢弃旧城市的迟到响应、一次刷新只产生一次请求。
- [列表条目以新对象替换或整表重建时，ForEach 键要包含会变且需要显示的字段](lesson-2e636699fa65aefd63f0.lesson.md)
  - 时机：功能实现与页面接线阶段，为可编辑或会重新拉取的列表选定条目更新方式与 ForEach 键时
  - 情境：列表条目编辑（如改名）后以保留 id 的新对象替换，或操作成功后重新请求列表并整表 setList（id 不变、计数等字段变化）；ArkUI 用 ForEach 渲染，并把条目字段作为子组件的 @Param 传入；源端是 Compose 不设 key 的 forEach 加不可变 copy，或 RecyclerView 整表刷新。
  - 例外：更新方式是对 @ObservedV2 条目的 @Trace 字段原地赋值，子组件绑定的仍是同一对象，此时可保留只含 id 的键
- [复用开关组件的变更事件给出目标值时，把它原样写入该开关的 setter，不改成无参回调再按旧值取反](lesson-40fc63b124b4a44e7a9f.lesson.md)
  - 时机：界面接线阶段，把开关行接入带 @Param isOn 与 @Event onToggleChange(nextState) 的复用组件，并连到 ViewModel 的开关接口时
  - 情境：源端每个开关点击时翻转自身字段、写偏好并刷新自身图标；目标复用组件在事件里给出下一状态，ViewModel 提供 toggleX() 取反接口，页面本地 @Local 与 ViewModel 各持一份开关值。
- [源端用带兜底的访问器取显示值时，目标调用已移植的等价访问器，不改读原始字段再自拟兜底](lesson-1fa08bf929cfced0ff34.lesson.md)
  - 时机：功能接线阶段，把源端刷新函数里的显示赋值（如 text = Manager.getX()）翻译成目标组件状态，或把登录判定与用户名显示映射成身份文案表达式时
  - 情境：源端在某一分支调用带空值兜底的访问器（如已登录但昵称为空时返回“用户{id}”或默认昵称），另一分支才显示“未登录”等占位文案；登录判定来自 token/session。目标侧会话或仓库层保留原始字段（昵称可为空），可能已移植同名兜底方法，组件状态是普通字段，工程里有现成的未登录占位字符串资源。也包括源端经工具类把数值码映射为显示文案（天气码、空气质量、风向）的情形。
- [源页面由事件订阅或结果回调触发的重新加载要迁成订阅；Navigation 根页或 Tab 内容在子页返回时不会再走 aboutToAppear](lesson-b3bb0bc33f4caded78a2.lesson.md)
  - 时机：ViewModel 与页面接线阶段，决定目标页由哪些入口触发数据重新加载时；流程闭环阶段从该页新增 push 子流程时
  - 情境：源 Fragment 用 EventBus @Subscribe（登录成功、记录变化等）和 ActivityResult 回调重拉数据；目标页是 Navigation 下常驻的根内容或 Tab 页，登录、详情等子页用 pushPathByName 覆盖后 pop 返回；工程已有会话状态与应用事件总线。
- [规格要求乐观更新时，先本地翻转状态再发请求，回调只用服务端真值回填](lesson-18c8e7630a96d66540bc.lesson.md)
  - 时机：界面交互实现阶段，编写收藏、点赞类切换的点击处理，确定本地状态翻转与服务端调用的先后时
  - 情境：验收要求点击后状态翻转、界面即时刷新（乐观更新）；源端把选中态设置写在网络接口的成功回调里；目标用状态变量驱动图标并异步调用接口。
- [迁移按状态切换的显示时同时迁移 setVisibility 分支：该状态下隐藏的控件不渲染，显示的区块要实现](lesson-43a9050245b1afa165bf.lesson.md)
  - 时机：界面实现与巡检修复阶段，迁移登录态等状态下控件的显示内容与显隐时
  - 情境：源端 Fragment 按登录态等状态对多个控件 setVisibility（如登录后隐藏用户名、显示签到区），部分 setText 被注释；目标 ArkTS 按状态条件渲染；工程可能有显隐或绑定检查器报告源控件丢失。
- [随状态变化的控件参数不作 @Builder 值参，改为内联读取状态或用 @ComponentV2 子组件的 @Param](lesson-8d2979542fa2cd65150c.lesson.md)
  - 时机：界面实现阶段（页面转换与公共组件抽取），为源端带状态参数的子控件或多个同构开关行选择 ArkUI 复用写法时
  - 情境：源端 Compose 子 Composable 以当前状态算出的值作参数（如 enabled = count &gt; 1、颜色随选中态变化），或 Android 页面有多个同构的开关行、各自持有状态；目标 ArkUI 组件需要在状态变化后刷新 enabled、颜色、开关图标等属性，准备把子控件或开关行抽成共享的 @Builder 方法。也包括用多参数 @Builder 渲染会被异步重新赋值的数组或对象（搜索结果、定位城市卡）的情形。
  - 例外：传入 @Builder 的只有文案、尺寸等在该组件生命周期内不随状态变化的值
- [页面向单例仓库或偏好注册监听时，把回调或句柄存成字段，在 aboutToDisappear 用同一引用移除](lesson-14b7f4090b7b83873b22.lesson.md)
  - 时机：功能接线阶段，在页面 aboutToAppear 里向应用级单例仓库、数据库或偏好注册数据监听时
  - 情境：目标数据层是应用级单例，用 addListener/removeListener（按回调引用移除）提供可观察数据；源端页面用 observeAsState、collectAsState 这类随界面生命周期自动结束的观察；ArkTS 子页出栈时不会自动注销。
- [页面直接读共享 @ObservedV2 模型的 @Trace 字段，不复制成 @Local 快照再手动同步](lesson-08c38f950b69e991607d.lesson.md)
  - 时机：功能接线与页面实现阶段，把页面显示状态接到 @ObservedV2 模型或共享 store，且模型会被其他页面、异步加载或服务回调改写时
  - 情境：目标端用 @ObservedV2 + @Trace 模型（AppStorageV2.connect 或单例 getter 取得）承载共享状态：源端由一个根状态持有者驱动多个屏幕，拆成 Navigation 下多个页面后由子页修改模型；或源端 Flow/StateFlow 持续推送列表与加载态，目标由异步加载、BLE/消息回调整体重新赋值 store 的 @Trace 字段，页面是 @ComponentV2 子组件。
  - 例外：需要与模型解耦的纯界面态（弹窗开关、未提交的输入草稿）仍放在页面 @Local

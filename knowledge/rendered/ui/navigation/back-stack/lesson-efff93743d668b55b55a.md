# 唯一页面被压在空的 Navigation 首页之上时，由栈底 NavDestination 自身的 onBackPressed 接管返回（不写在 @Entry 页，@Entry.onBackPress 收不到）：size()<=1 时 moveAbilityToBackground 退后台、不出栈露出空白宿主；源端未覆写返回时按 Activity finish() 同时执行 onDestroy 的释放并复位页面实例态，参照设备实测为 HOT 恢复时才保留实例

## 何时使用

规格提取与入口装配阶段，为单 Activity 应用确定根页面的返回语义、搭建 Navigation 入口壳并决定首页放在 Navigation 内容区还是首次 push 时；页面转换阶段为首启引导页、主菜单等可能成为栈底的页面接返回时；把注入经验转成派工要求、确定栈底返回的生命周期效果时

## 适用情境

安卓启动 Activity 未覆写 onBackPressed，也没有 OnBackPressedDispatcher、BackHandler 或 KEYCODE_BACK 处理（含 Compose NavHost 的起始目的地），返回键走 Activity 默认行为：默认 finish()，onDestroy 执行（如释放音乐、关闭数据源），实例态（输入框文字、所选值、播放位置）丢失，进程与静态单例保留；部分 Android 12+ 设备与启动方式下任务根 Activity 改为移到后台、onPause 存档、onResume 读档，以参照设备实测为准。目标按 Navigation + NavDestination 模板，用内容为空的 Navigation 首页在启动时 pushPathByName 压入唯一页面，或启动页已生成为 NavDestination、入口只能首次 push。也包括源端根 Activity 自己注册按状态启用的 OnBackPressedCallback（如锁屏时只提示、暂停预览时恢复、先关弹出面板），未消费时才走 Activity 默认行为，目标根页同样由入口 Navigation 首次 push。

## 原因

“空栈时返回退出应用”只对 Navigation 首页成立；唯一页面被压栈后栈深为 1，返回会把它弹出，露出空白首页，应用仍在前台。栈内有 NavDestination 时返回先交栈顶 NavDestination，返回 false 即出栈，@Entry 页的 onBackPress 不会被调用，把兜底写在 @Entry 页等于没写。来源中“由根页接管”被三个 agent 读成 @Entry 入口页，“按 Activity 默认退到后台”被规格写成“默认退后台”。把“Activity 默认返回”一律当成退后台，还会漏掉 finish() 的释放与复位：再次进入仍保留输入框文字、所选值与音乐播放位置；改用 terminateSelf 又会结束鸿蒙进程、丢失源端保留的静态局面。另一应用中注入的一行提醒被编排者写进派工当作源码事实，参照设备（以 am start 启动的 SDK 37 模拟器）实测却是 finish。

## 做法

1. 在每个可能成为栈底的 NavDestination（冷启首页、首启引导页、清栈回根后的页，或它们共用的裁决函数）的 .onBackPressed 中按栈深判断：navPathStack.size() <= 1 时取 UIAbilityContext 调用 moveAbilityToBackground() 并 return true，消费返回、不出栈（不用 terminateSelf，以保留进程与静态单例）；不写在 @Entry 页的 onBackPress。源端未覆写返回时同时执行源 onDestroy 的释放并把页面实例态复位到 onCreate 初值，下次 onShown 重走 onCreate 的初始化，只有参照设备实测返回后再启动是 HOT 恢复原实例时才省略复位。栈深大于 1 时不拦截；页面上的对话框或抽屉打开时先由它们消费返回。
2. 源端有返回处理（onBackPressed 覆写，或按状态启用的 OnBackPressedCallback）时按源端逻辑实现：由状态拥有方（如 ViewModel）提供一个按源端回调优先级返回“是否已消费”的裁决方法，栈底 NavDestination.onBackPressed 先关页内覆盖层、再调用它，都未消费才走上一步的栈深分支；宿主页由其他任务负责时把这条接线登记为移交，不用“由 Navigation 返回拦截承载”一类注释代替实现；对 onBackPressed 的可用 API 版本有疑问时查本机 SDK 声明或编译验证，不因猜测回避。首屏不必是 NavDestination 时，也可把它作为 Navigation 根内容常驻、不压栈，空栈返回按系统默认处理。
3. 列出所有会把栈收成只剩根页的路径（冷启动首次 push、首启引导、深链清栈重建、删除或克隆后清栈回根），确认它们都由同一个栈底返回处理接管，不只覆盖冷启动。
4. 规格提取时，源端根页没有返回处理、依赖 Activity 默认行为，也要在导航规格写出栈底返回的可验收项，锚点指向栈底页的 onBackPressed，不写“系统默认/默认退后台”：列出 finish 的可观察效果（onPause、onStop、onDestroy 各做什么，哪些实例态回初值，哪些静态单例保留），无法确认参照行为时把“返回后再启动的页面状态”写成待核验收项；编排派工不把经验的通用结论写成“源 Activity 默认 = …”的源码事实。

## 可选检查

- 冷启动后按一次返回：应用退到桌面且进程与静态局面保留，再次进入时页面实例态与参照设备一致（finish 时回到初值）；出现空白页或应用仍在前台，说明返回链路漏接。

来源支持：5 张卡 · 已知 4 次迁移（部分未记录） · 已知 4 个应用（部分未记录）

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；安卓 Android SDK 源码 android-36.1。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕NavDestination 的 onBackPressed 只在与 Navigation 绑定的路由栈里有页面时生效；回调返回 true 表示页面自己处理返回、不出栈，返回 false 表示回退到上一个页面（当前页出栈）。〔成立范围：对 NavDestination 组件的 onBackPressed（API 10 起）；Navigation 首页（NavBar）不在路由栈里，没有这个回调；最常见的不成立情形：栈里已没有 NavDestination（只剩首页）时，返回不经过任何 onBackPressed。〕
- 〔原因〕Navigation 直接挂载的子节点是导航栏（NavBar），单栏显示时就是首页；NavBar 不在页面栈 NavPathStack 中、不具备页面生命周期，也不能用 NavPathStack 的方法控制，因此 size() 只数压入的 NavDestination：首页压入唯一页面后 size() 为 1，这一页出栈就露出首页。〔成立范围：对 Navigation + NavPathStack 的单栏显示；最常见的不成立情形：分栏显示时 NavBar 是固定显示的导航栏，子页出栈后不是「露出首页」而是内容区变空；hideNavBar(true) 时栈空显示空白。〕
- 〔做法第 2 步〕UIAbility.onBackPressed（侧滑或按返回键退到 UIAbility 层时回调）未覆写时：targetSdkVersion ≥ 12 默认返回 true，UIAbility 被移到后台、不销毁；targetSdkVersion < 12 默认返回 false，UIAbility 被销毁。〔成立范围：对未覆写 onBackPressed 的 UIAbility，因此 Navigation 空栈时「按系统默认处理」在 targetSdkVersion ≥ 12 的工程里是退后台、实例和页面状态都保留，不等于安卓的 finish；最常见的不成立情形：targetSdkVersion < 12 的工程默认销毁。〕
- 〔做法第 1 步〕UIAbilityContext.moveAbilityToBackground() 把处于前台的 UIAbility 移到后台（不销毁），只能在主线程调用；从 API 13 起只在 Phone、Tablet、Wearable、TV 上可正常调用，其他设备返回错误码 16000061，UIAbility 不在前台时返回 16000065。〔成立范围：对 moveAbilityToBackground（API 12 起；API 12 时 Tablet 也返回 16000061）；它返回 Promise，失败不会反映到 onBackPressed 已同步返回的 true 上；最常见的不成立情形：在 PC/2in1 等不在上述列表里的设备上调用失败，返回已被消费，界面无反应。〕
- 〔做法第 1 步〕应用从后台回到前台时，栈顶 NavDestination 触发 onShown、不触发 onWillShow；退到后台时触发 onHidden、不触发 onWillHide。从 API 21 起 onShown / onHidden 的回调参数 VisibilityChangeReason 为 APP_STATE（前后台切换）、TRANSITION（页面跳转）或 CONTENT_COVER（全模态开关）。〔成立范围：对 NavDestination 的可见性回调；API 21 之前回调没有原因参数；最常见的不成立情形：把「下次显示时重走 onCreate 的初始化」放在 onWillShow，moveAbilityToBackground 后再回前台时不会执行。〕
- 〔适用情境〕安卓 Activity.onBackPressed 的默认实现随平台版本不同：Android 12（API 31）之前 finish 当前 Activity；从 Android 12 起，任务根 Activity 且在清单里声明了 ACTION_MAIN + CATEGORY_LAUNCHER 的 intent-filter 时，Activity 连同任务被移到后台而不 finish，其他 Activity 照旧 finish。〔成立范围：对没有覆写 onBackPressed、也没有注册返回回调消费返回的 Activity；默认实现先收起已展开的 ActionBar actionView、再弹框架 FragmentManager 的回退栈，两步都没发生才按 finish 或移到后台处理；版本条件取自 Activity#onBackPressed 的文档说明（实际判定在系统服务里，SDK 源码看不到）；最常见的不成立情形：Activity 不是任务根（例如被别的应用拉起在对方任务里）时按 finish 处理。〕

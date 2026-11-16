# 启动与外部入口

读到 AndroidManifest 里的 LAUNCHER、深链 intent-filter、navDeepLink，闪屏或跳板 Activity、入口 onCreate 的启动分支，或桌面小组件等系统表面，规格里写冷启动路由、再次拉起、深链和外部入口时

## 触发族

- [清单里的深链 intent-filter](deep-link-intent-filter/index.md)（5 条）：读到 AndroidManifest 里带 VIEW / BROWSABLE、android:scheme / host / autoVerify 的 intent-filter，或导航模块里的深链路由器；规格里写深链的应用壳契约、skills.uris、domainVerify、锚点和验收拉起法
- [LAUNCHER 跳板和再次拉起](launcher-entry/index.md)（4 条）：读到 LAUNCHER Activity 是无界面跳板或 SplashActivity，按条件 startActivity 后 finish，Intent 带 CLEAR_TOP / NEW_TASK|CLEAR_TASK；规格只写冷启首帧前选路由，没写再次拉起、最近任务切回、CLEAR_TOP 生效场景或加载页的最短可见时长
- [桌面小组件等系统表面的应用内替代页](system-surface-replacement/index.md)（1 条）：读到源端的 AppWidgetProvider 桌面小组件等系统表面在应用内没有入口，决策把它降级为新的应用内页面；决策台账或规格只写了替代页的加载和跳转，没写入口位置、形式和对已对等页面的影响
- [启动判定里的登录态和首启分支](launch-login-branch/index.md)（3 条）：读到闪屏或启动 Activity 用 when / if 按持久化的用户信息、token、引导完成、已选列表是否为空分支跳转；规格只照搬 when 分支，没列各状态组合的去向、无已选项的首启行为，或加了源端没有的 token 拦截分支却没登记
- [入口 onCreate 里 super.onCreate 之前的调用](pre-super-oncreate/index.md)（1 条）：读到入口 Activity.onCreate 在 super.onCreate / setContentView 之前调用 setTheme(...) 等；规格只写设置页保存后即时生效，没写冷启动首帧前恢复和目标承接位置
- [由常量拼出的深链和分享链接 URI](deeplink-uri-constants/index.md)（1 条）：读到 navDeepLink { uriPattern = "$常量/路径/{id}" } 或复制链接的字符串由域名常量拼出；页面数据、规格或 AC 里出现源码中没有的自定义 scheme，没写常量展开后的地址
- [清单 intent-filter 声明的外部动作和分享接收](intent-filter-share-actions/index.md)（3 条）：读到 AndroidManifest 入口 Activity 下的多条 intent-filter（SEND、SEND_MULTIPLE、SEARCH、PROCESS_TEXT、自定义 scheme 的 VIEW）和代码里读的 EXTRA_TEXT / EXTRA_STREAM / EXTRA_SUBJECT；规格把它们合成一条 sendData skill、按 want.parameters 自造键取数，或写成不路由
- [外部入口的实例形态和分发时机](entry-instance-dispatch/index.md)（3 条）：读到源入口 Activity 没写 android:launchMode（standard）、只在 onCreate 读 getIntent() 处理完就 finish()，或入口 Intent 在密码门之后才处理；规格写 EntryAbility onCreate / onNewWant 解析 want、launchType singleton、「冷启动 / 热启动」，没写已运行时再收到 want、结束的是哪个实例和分发的前置条件

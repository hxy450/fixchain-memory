# LAUNCHER 跳板和再次拉起

agent 会看到什么：读到 LAUNCHER Activity 是无界面跳板或 SplashActivity，按条件 startActivity 后 finish，Intent 带 CLEAR_TOP / NEW_TASK|CLEAR_TASK；规格只写冷启首帧前选路由，没写再次拉起、最近任务切回、CLEAR_TOP 生效场景或加载页的最短可见时长

## 规矩

- rule-968de12c3958｜入口分流的规格按冷启、回收重入、运行中桌面再拉起、最近任务切回逐种写验收｜读到：LAUNCHER Activity 是无界面跳板，manifest 未声明 launchMode（缺省 standard）；应用内用 TaskStackBuilder.startActivities 或 NEW_TASK|CLEAR_TASK 改写任务根；写错：规格和验收条目只写「EntryAbility 首帧加载前（loadContent 之前）选入口路由」这一种冷启分流，没有进程存活时从桌面图标再次拉起的分支，也没写单例 UIAbility 再次拉起走 onNewWant、页面栈原样保留
- rule-d848f5b9eaab｜跳板带 FLAG_ACTIVITY_CLEAR_TOP 时，规格写明它生效的进入场景，不写成「根页天然唯一」｜读到：LAUNCHER 跳板 Activity 按条件 startActivity 后 finish，跳往主页的 Intent 带 addFlags(FLAG_ACTIVITY_CLEAR_TOP)；写错：规格把 CLEAR_TOP 映射成「主页是 Navigation 根页、天然栈内唯一，无需显式清栈即可满足语义」，没写它在哪种进入场景生效、生效后清掉哪些页面
- rule-b97722aedb0f｜用户要求「和源端一样有加载页」时，规格把首次冷启动的最短可见时长写成验收项｜读到：用户要求首次启动和安卓一样有页面加载；源端 SplashActivity 继承外部 SDK 的启动 Activity，SDK 初始化走完才启动 MainActivity；目标端初始化只读本地配置；写错：验收标准只要求首帧进度状态，或写「不通过人为延迟伪造用户可见行为」，没写首次冷启动的最短可见时长，也没登记为决策缺口
- rule-6917cd1524c4｜外部入口 Intent 带 FLAG_ACTIVITY_CLEAR_TOP 时，规格写出热启动先清上层页的后果｜读到：桌面卡片等外部入口的显式 Intent 带 FLAG_ACTIVITY_CLEAR_TOP | FLAG_ACTIVITY_NEW_TASK 拉起主 Activity；写错：规格只保留 flag 字面，或后果只写「进入某 tab」「冷启动与运行期 want 均覆盖」，没写应用在前台压着详情页时要先清掉详情栈

# 退出登录钩子先停并等同步，再单事务清账号业务表，最后广播数据变化

审的是：代码
触发（任一种）：
- 读到：安卓源的退出登录方法除清 token 和账号 SharedPreferences 外，还调用本地数据库的 removeAll 清业务表；或者读到的旧目标实现的会话清理只清 preferences 和登录态；写错的样子：目标的退出/会话清理钩子只清 preferences、登录态、网络缓存并发登录状态事件，没有先停止并等待同步，没有在 RdbStore 里清按账号归属的业务表，也没有广播数据变化
适用范围：迁移或重构退出登录、账号销毁、游客重建的会话清理钩子时
做法：
- 钩子第一步停止并等待同步任务结束，之后才动本地数据
- 对照源端退出调用的数据库清理，列出所有按账号归属的本地状态（业务表、游标、同步队列、搜索历史、订阅等），在一个 RDB 事务里逐项清掉；不属于账号的静态表保留
- 清完后广播数据变化事件，让已打开的页面重新查询
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 停止并等待同步 → 一个 RDB 事务里清事件、完成态、子任务、游标、订阅、同步队列、搜索历史等账号数据，保留图标、颜色这类静态表 → 广播数据变化事件：卡里最终保留的清理顺序；改前退出后首页重新查询仍显示旧用户数据（出处：卡里修好并验证过）
- beginTransaction(): void：RdbStore 开启事务（出处：鸿蒙 SDK 的 ets/api/@ohos.data.relationalStore.d.ts，RdbStore.beginTransaction）
- commit(): void；rollBack(): void：RdbStore 提交、回滚事务（出处：鸿蒙 SDK 的 ets/api/@ohos.data.relationalStore.d.ts，RdbStore.commit、RdbStore.rollBack）
- delete(predicates: RdbPredicates): Promise<number>：RdbStore 按谓词删行，返回删掉的行数（出处：鸿蒙 SDK 的 ets/api/@ohos.data.relationalStore.d.ts，RdbStore.delete）
- deleteSync(predicates: RdbPredicates): number：同族接口：RdbStore 的同步删行（出处：鸿蒙 SDK 的 ets/api/@ohos.data.relationalStore.d.ts，RdbStore.deleteSync）
针对本应用要查的：
- 源端退出时清了哪些本地数据：源工程里退出登录方法及它调用的数据库初始化/清理类，找 removeAll、清表、清 SharedPreferences 的调用；逐个列出被清的表和偏好，按账号归属的都要在目标的清理事务里有对应的一项
来源：1 张卡，1 个应用
- case-6c62d7c44b9a82b2388c（记得日历）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 2、建议 3、诊断；做法第 3 步 ← 建议 3、诊断；取值 1 ← 诊断

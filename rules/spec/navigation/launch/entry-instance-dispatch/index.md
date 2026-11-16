# 外部入口的实例形态和分发时机

agent 会看到什么：读到源入口 Activity 没写 android:launchMode（standard）、只在 onCreate 读 getIntent() 处理完就 finish()，或入口 Intent 在密码门之后才处理；规格写 EntryAbility onCreate / onNewWant 解析 want、launchType singleton、「冷启动 / 热启动」，没写已运行时再收到 want、结束的是哪个实例和分发的前置条件

## 规矩

- rule-9737a4fd2ca4｜源 standard、目标 singleton 时，规格单列「已运行时收到新 want」场景｜读到：源 Activity 没设 `android:launchMode`（standard），每个外部 intent 都新建 Activity，在 `onCreate` 读 `getIntent()` 并 `setResult`；规格把目标 `launchType` 定为 singleton；写错：规格服务层只写 `onCreate` / `aboutToAppear` 里解析 want，没有「已运行时再收到外部 want（onNewWant）」的条目
- rule-a175acb350b1｜SEND 分享入口在 standard Activity 上时，规格写明每次新建独立实例、只结束自己｜读到：清单 Activity 上有 action SEND / SEND_MULTIPLE + category DEFAULT + mimeType 的 intent-filter，没写 launchMode（standard）；源码没有 onNewIntent，只在 onCreate 读 getIntent() 的 EXTRA_TEXT，处理完 finish()；写错：规格写「EntryAbility onCreate/onNewWant 解析 want → 路由本页」「冷启动/热启动」，结束只写 setResult+finish 或 → terminateSelf，没写结束的是哪个实例
- rule-45fe76b36be1｜入口分发 AC 照抄源端前置条件：源端在锁屏密码门之后才处理入口，落库动作写明「门之后」｜读到：源端入口 Intent 的处理在密码门受理之后才被调用；写错：规格的快存、分享落库 AC 只写「无 UI 落库」，没写「密码门之后」，实现把落库放进 EntryAbility 冷启 dispatch 里

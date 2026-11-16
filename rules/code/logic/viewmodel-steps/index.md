# 源 ViewModel 方法在请求、提交前后的步骤

agent 会看到什么：读到源 ViewModel 的方法在请求前查库回填参数、提交时先经 Repository 写入、推进后预取图片，或在弹层 onExpanded 时才加载，交回的代码少了这一步或换了调用时机（只 showToast、直接用传入对象的字段、页面初始化就请求）

## 规矩

- rule-aee385036b64｜组装请求参数前核对经纬度来源，只有 ID 或经纬度为空时先查库补齐｜读到：源端 ViewModel 请求前用 DAO 的按 ID 查询（@Query）回填 `lon` / `lat`；写错：目标直接用传入城市对象的 `lon` / `lat` 构造请求，首页和详情跳转都取它；对象只有 ID 时请求带空经纬度
- rule-b254ef790454｜源端操作写入仓库后才提示成功时，目标先写入共享状态再 showToast，不用成功提示占位｜读到：ViewModel 的提交方法先校验参数，再经 Repository 写入（同键累加、新项追加），最后关闭弹层并提示成功；写错：确认分支里只有 showToast(...) 的成功提示，Service 里没有对应的写入方法，也没有写到别的页面能读到的状态
- rule-7358976d7217｜源弹窗展开后才加载数据时，目标先打开弹层再在弹层内异步加载，带加载中和失败重试｜读到：源端弹窗组件的 onExpanded 回调里才调用 ViewModel 的加载方法，打开只置 visible，失败可重试（onRetry）；写错：目标在页面初始化（aboutToAppear 的加载函数）里就请求、catch 后静默置空无重试；或打开前先 await 网络再把 showSheet 置 true
- rule-e96373e53ee1｜源 ViewModel 推进后主动预取后续几张图时，目标 ViewModel 实现预解码并给缓存设上限｜读到：源 ViewModel 在加载完成和每次推进后调预取方法：排除已处理、已跳过、有挂起变更的项和视频，取后续 3 项，用 Coil 的 imageLoader.enqueue 预取到内存缓存；写错：目标 ViewModel 里没有任何预加载字段、方法或调用；页面只用 Image 组件按需显示当前项
- rule-996d0f307b4a｜源端按 id 在仓库层查出的派生值，目标也按 id 查，不改成调用方传入或写死空串｜读到：源端用 id 到仓库层（Repository）查出派生值，如按 id 取显示标题作快捷入口 label；写错：目标深链分支把该值写死成 `''`，或改成由调用方传入；风险里承认值为空，却没登记占位

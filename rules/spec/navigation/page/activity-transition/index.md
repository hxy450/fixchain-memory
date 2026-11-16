# Activity 跳转的转场动画

agent 会看到什么：读到源 Activity 用 startActivity / finish 跳转，源码里没有 overridePendingTransition、styles 没覆盖 windowAnimationStyle，或本类和基类 onCreate 里 overridePendingTransition(0, 0)；规格的导航关系、ui-graph、路由契约写「无转场」、transition_anim 填 "none"，或 pushPathByName 没带 animated=false

## 规矩

- rule-c29d9f8f0cd3｜源 Activity 跳转没自定义转场时，规格写平台默认动画和各页 pageTransition 目标值｜读到：源端多个 Activity 用 startActivity 跳转、finish 返回，源码里没有 overridePendingTransition，styles 也没覆盖 windowAnimationStyle；写错：规格的导航关系、ui-manifest 只写「router.pushUrl 页面跳转」，或写「无转场」，没有页面切换动画这一项，也没给 pageTransition 的目标值
- rule-44d9577c83b8｜源端没自定义转场时，transition_anim 写 platform-default，不写 none｜读到：源码没有 overridePendingTransition，也没有 res/anim 下的转场引用；写错：ui-graph 导航边的 transition_anim 一律填 "none"
- rule-a4ca3df4446b｜源 Activity 或基类 onCreate 关进入转场时，规格记成目的地属性并写进每条路由契约｜读到：源 Activity 或它继承的基类在 onCreate 里调 overridePendingTransition(0, 0)；写错：规格只把转场禁用挂在抽屉基座的 AC 上，或只记了本类 onCreate 调用的那几页；进入该页的路由契约写成 pushPathByName / replacePathByName 两参，没有 animated=false，目的地页规格也没写「进入无转场」
- rule-3beaad7f2598｜规格的导航、显隐类验收条目要附转场契约：资源、时长、插值器、起止、覆盖关系｜读到：源码进入详情、覆盖页面或显隐时有 setCustomAnimations、startAnimation、res/anim 资源、config_mediumAnimTime 等时长；或页面级 UI spec 写「动画对齐 animateTransition(…)」；写错：feature 规格的导航、显隐类 AC 只写路由等价（「→ navPathStack 路由」「…等价」）或「隐藏」，没有源动画资源、时长、插值器、起止状态和谁覆盖谁

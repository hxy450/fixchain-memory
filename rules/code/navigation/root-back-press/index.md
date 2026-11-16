# 根页的返回键（启动 Activity 没覆写 onBackPressed）

agent 会看到什么：读过的源码里启动 Activity 或根 Activity 没覆写 onBackPressed、没有 OnBackPressedDispatcher，返回即 finish，onDestroy 里有释放；交回的根 NavDestination 没有 .onBackPressed、按返回露出空白首页，或只 moveAbilityToBackground 而没做释放，或调了 terminateSelf

## 规矩

- rule-24ddf7c773e8｜启动 Activity 没覆写返回时，根页 onBackPressed 里移到后台并返回 true｜读到：启动 Activity 没有覆写 onBackPressed，没有 OnBackPressedDispatcher 回调，onKeyDown 也不处理 KEYCODE_BACK；存档写在 onPause、读档写在 onResume；写错：入口页是 Navigation(this.navPathStack){} 空首页，aboutToAppear 里 pushPathByName 压入唯一页面；该 NavDestination 没有 .onBackPressed，按返回出栈露出空白首页
- rule-5ccd4b236357｜根页按 finish 返回时，先做 onDestroy 释放和复位，再 moveAbilityToBackground｜读到：源根 Activity 没有覆写 onBackPressed，onDestroy 里有 release() / close()；写错：NavDestination 的 onBackPressed 在栈深≤1 时只调 moveAbilityToBackground() 并 return true，onDestroy 的释放只挂在 aboutToDisappear 上

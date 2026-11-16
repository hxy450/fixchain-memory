# 根 Activity 没覆写的返回键

agent 会看到什么：读到启动页或任务根 Activity 没有覆写 onBackPressed / onKeyDown，或抽屉关闭时调 super.onBackPressed()；规格的返回契约或 AC 写「退后台，不出栈」「系统返回默认」

## 规矩

- rule-82fdb207dde2｜源根 Activity 没覆写返回时，规格的返回契约先列 finish() 的效果，不直接写退后台｜读到：源启动 Activity 没有覆写 onBackPressed / onKeyDown，onDestroy 里有 release() / close()，页面持有 EditText 文字、所选值、背景音乐等实例态；写错：规格写「源 Activity 默认：退后台，不出栈」，或把「栈深≤1 时 moveAbilityToBackground 不 pop」写成验收项，没写返回会触发 onDestroy、实例态回到初值
- rule-a8b4ed77442a｜源端任务根页无返回处理时，规格把栈底退后台锚到栈底页 onBackPressed，不写“系统默认”｜读到：源端任务根 Activity（首启引导、主菜单等）没有覆写 onBackPressed，或抽屉关闭时调 super.onBackPressed()；目标入口 @Entry 页是空内容的 Navigation 宿主，启动时 pushPathByName 压入首个 NavDestination；写错：规格的 AC 或契约写“源端无返回拦截照搬”“系统返回默认”“抽屉关→false（走默认）＝退后台”，没写由哪个回调实现退后台
- rule-c62478d4f8fd｜规格的页面跳转表补「系统返回」行：根页退到后台或退出，有弹层先关弹层｜读到：源端有可被 Back 关闭的对话框、popup，或根 Activity 注册了 OnBackPressedCallback；写错：页面跳转表没有「系统返回」行，或只写「系统返回 → pop」，没区分根页和有弹层的情形

# main_pages.json 的 src 页面登记

agent 会看到什么：源端导航图里的目标 Fragment、底部导航或 DialogFragment，目标 main_pages.json 的 src 登记了哪些文件：router.pushUrl 的目标页、被 import 的 Tab 子组件和 @CustomDialog，以及编译报 10905402

## 规矩

- rule-b09dd43fa981｜router.pushUrl 跳到的目标页，要在 main_pages.json 的 src 里登记｜读到：源端导航图里的目标 Fragment（`navigate(R.id.…)` 跳到的详情页、编辑页）；写错：代码里 `router.pushUrl({ url: 'pages/…' })` 的目标页没有出现在 `resources/base/profile/main_pages.json` 的 `src` 数组里
- rule-ad04c88863e6｜main_pages.json 只登记路由页，被 import 的 Tab 子组件和 @CustomDialog 不登记｜读到：源端单 Activity 用 BottomNavigationView + NavHost 承载底部导航 Fragment；写错：main_pages.json 的 src 列了所有页面文件，包括被主页面 import 进 TabContent 的 @Component export struct 和 @CustomDialog

# router.pushUrl 跳到的目标页，要在 main_pages.json 的 src 里登记

审的是：资源
触发（任一种）：
- 读到：源端导航图里的目标 Fragment（`navigate(R.id.…)` 跳到的详情页、编辑页）；写错的样子：代码里 `router.pushUrl({ url: 'pages/…' })` 的目标页没有出现在 `resources/base/profile/main_pages.json` 的 `src` 数组里
适用范围：目标端用 router 按 url 跳转的每个页面
做法：
- 在 main_pages.json 的 "src" 数组里加上 "pages/<目标页>"，写法与 pushUrl 的 url 一致（路径以模块的 src/main/ets 为基准）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- src：当前 Module 所有页面的路由信息，页面路径以当前 Module 的 src/main/ets 为基准，取值是字符串数组：pushUrl 的 url 要在这个数组里（出处：module-configuration-file.md，pages标签）
- "pages": "$profile:main_pages"：module.json5 里指向 resources/base/profile/main_pages.json（出处：module-configuration-file.md，pages标签）
- 100002 - Uri error. The URI of the page to redirect is incorrect or does not exist：pushUrl 的 url 写错或页面不存在时报的错误码（出处：鸿蒙 SDK 的 ets/api/@ohos.router.d.ts，router.pushUrl）
来源：1 张卡，1 个应用
- case-be539ffd7751410d8ad6（星途清单）：做法第 1 步 ← 建议 1

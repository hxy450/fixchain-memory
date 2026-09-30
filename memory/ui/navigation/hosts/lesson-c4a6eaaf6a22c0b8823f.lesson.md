# main_pages.json 只登记经 router 进入的 @Entry 页：被 Tabs/父页导入的子组件与 @CustomDialog 不登记，10905402 与 @Entry+export 警告先判定角色

ID：`lesson-c4a6eaaf6a22c0b8823f` · 版本：2

[本主题](index.md)

## 何时使用

入口装配阶段写 main_pages.json 路由登记时；编译修复遇到“登记页面须有且仅有一个 @Entry”（10905402）或“export struct with @Entry”警告时

## 适用情境

源端单 Activity 以底部导航承载多个 Fragment，另有 DialogFragment 与经导航跳转的二级页；目标主页面用 Tabs/TabContent import 并实例化页面 struct，弹窗写成 @CustomDialog，这些文件都放在 pages/ 目录；工程用 main_pages.json 登记路由页。

## 原因

main_pages 的每个登记项都被当成路由页，必须恰有一个 @Entry。按 pages/ 目录全部登记，会让 Tab 子组件和弹窗背上路由页约束；为过编译给它们补 @Entry 又保留 export，形成 @Entry+export 角色冲突；去掉 export 又破坏父页导入，修复就在两者间摇摆。来源中弹窗漏补 @Entry 使构建失败，Tab 页的警告一直留到用户在 IDE 里看到；最终为消警告把 Tab 内容内联进主页时，又用只有标题和 TODO 的 builder 顶替了三个 Tab 页。

## 做法

1. 写 main_pages 前逐文件判定角色：被其他 .ets import 并在 Tabs 或父组件中实例化的 struct 是子组件（@Component export，不登记）；经 router.pushUrl 进入的才是路由页（@Entry、不 export、登记）；@CustomDialog 由宿主页弹出，不登记。
2. 遇到 10905402 时，以 main_pages 实际 src 列表逐项检查：该文件被导入作子组件或是弹窗，就移除登记；确为路由页才补 @Entry，并去掉 export、确认没有导入方。若出于既有约束保留某弹窗的登记，就同时保证它恰有一个 @Entry，登记与装饰器一起改。
3. 同一内容既做 Tab 又要单独路由时，抽出 export 的 @Component 供 Tab 使用，另写 @Entry 外壳页包装它；不要用占位 builder 顶替原页面内容。


# 共享组件挂到哪些页面，以源码里的实际挂载为准（含布局声明的 Fragment 与导航图）；模板示例和上游说法不是依据

ID：`lesson-34c8ac69ad849f8c24e1` · 版本：4

[本主题](index.md)

## 何时使用

功能索引、规格提取与接线规划阶段，确定播放条等 Fragment 型共享组件挂载到哪些目标页面时；页面转换阶段收到要求建槽位的派工时

## 适用情境

源端共享组件只被个别宿主挂载：宿主代码把 Fragment replace/add 进自己布局的容器 id，主布局没有对应容器；流水线模板示例、功能索引或派工里写着“主页(某组件)常驻”一类通用说法。

## 原因

模板示例来自别的应用，写进功能索引后会沿规格、接线计划和派工一路传成“事实”；后续的规格作者与页面转换者即使读到主布局没有对应容器，也倾向保住上游说法（把验收锚点改挂到无关源行、按“常见位置”放槽），目标页多出源端没有的组件。

## 做法

1. 每条“组件 → 页面”关系先在源码中找到实际挂载，以下都算：宿主代码对容器 id 的 replace/add 调用；布局里的静态 <fragment>，由 FragmentManager 按 class 或 android:name 直接实例化（android-36.1 android/app/FragmentManager.java 的 onCreateView）；AndroidX FragmentContainerView 的 android:name，加载布局时由框架创建该 Fragment 并提交添加事务（androidx-main FragmentContainerView.kt 类注释，2026-10-15 访问）。android:name 是 NavHostFragment 时，沿 app:navGraph 或代码里的 setGraph 找到导航图，再按导航调用和实际可达路径确定各目的地挂在哪个宿主；图里声明了目的地只说明导航关系，不代表它常驻在宿主的每个页面。都找不到才不写。
2. 上游索引或派工声称某页有某组件、源码却找不到对应挂载时，登记为待决冲突交裁决；不要把验收锚点改挂到无关源行来保住这条要求。
3. 页面转换时派工要求的槽位在源布局中不存在，在回报里列为冲突并请求确认，不自行放到“常见位置”。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-3db1068ed462e12cf813](../../../store/cases/case-3db1068ed462e12cf813/e619d9487fd9bdbba6d0959e7b2935f08c667fed9eb9dc3d02e929ea5fc2076a.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`e619d9487fd9bdbba6d0959e7b2935f08c667fed9eb9dc3d02e929ea5fc2076a`

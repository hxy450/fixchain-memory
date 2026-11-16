# 切片计划与重构计划

交回的是切片计划、重构计划、批次与模块拆分或改动清单：scope、acceptance、integration_points、Step、跨业务依赖，以及换了承接方的源端职责时

## 触发族

- [重构计划的跨业务依赖](refactor-dependency-map/index.md)（1 条）：重构计划里的跨业务依赖模拟：是手写的依赖骨架，还是当前代码里页面、ViewModel、Service 之间真实的 import 和路由跳转
- [切片计划里带入的规格条目](slice-spec-carryover/index.md)（5 条）：功能或页面规格里写了交互验收、触发时机、事件通道或导航关系，切片计划的 scope、acceptance、integration_points、Step 或接线派工里缺了这一项
- [换了承接方的源端职责](reassigned-responsibility/index.md)（3 条）：源端一项职责在目标里交给另一切片的服务或换成平台替代（WorkManager 聚合状态、三方 MapView），承接方的派工或计划里没有对应的任务和验收条款
- [重写和重构计划的规格范围与模块拆分](refactor-plan-scope/index.md)（3 条）：重写或重构的计划（refactor-plan、批次、模块拆分）里，规格索引中已批准但仍是 planned / pending 的规格、功能清单的分组，怎么落成批次任务、验收项和模块
- [经公共构建器注册的新条目](builder-side-effects/index.md)（1 条）：源端新条目和兄弟条目一样经公共构建器函数注册，计划的改动清单只映射了调用处看得到的显式配置
- [经公共构建器注册的新条目的按 key 登记表](builder-key-tables/index.md)（1 条）：目标端同类能力按 key 登记在多个文件的白名单或映射表里，计划的改动清单漏了含同构建器兄弟 key 的某张表

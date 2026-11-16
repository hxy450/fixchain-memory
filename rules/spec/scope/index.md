# 迁移范围与功能归属

规格里写迁移范围、功能归属（page_id ownership、归某 feature）、功能入口页、跨页面共享组件、别的规格留给本文档承接的条目，或引用上游清单和台账（api-inventory、skip-list）时

## 触发族

- [功能入口页上的红点、数量和角标](entry-badge-state/index.md)（2 条）：安卓入口页（如「我的」页 Fragment）除了 startActivity 跳转，还按接口字段、登录状态 setVisibility 显示这个功能的红点、数量或角标，规格、Gate 摘要和验收清单只覆盖功能页内部、把入口记成「既有路由」
- [别的规格或契约里定义、留给本文档承接的条目](cross-spec-handoff/index.md)（3 条）：读到共享谓词的完整条件只写在别的规格的 AC 里、跨模块契约把某个 seam 标「待 Feature Spec」、AC 范围疑似归属别的功能；交回的消费页规格、feature spec 或 UT 设计只写了名字或笼统说法，或按字面写成 RED 用例
- [源端入口委托的跨页面共享组件](shared-component-delegation/index.md)（1 条）：读到源端入口把点击委托给跨页面共享的详情对话框或分享弹层；审计或真值整理按当前页自有 API 逐项判定，把共享组件里的动作写成「应禁用或报未实现」
- [规格引用的上游清单和台账条目（api-inventory、接口清单、skip-list）](upstream-list-references/index.md)（3 条）：读到模板或派工要求取 api-inventory.json 的 auth_type、接口清单的常量表、上游 skip-list 里「无 X API」的条目，而磁盘上只有 raw_apis.json、查出来是 0 条或作者自己没检索过 d.ts；交回的规格照样写「见某数据源」「已就绪」或照抄「无 X API」
- [源端行为、页面和接口归到哪个 feature](feature-ownership/index.md)（6 条）：读到源页面有已确认的活行为、接口文档列着 POST 端点及调用位置，或页面同包里有自己的 Retrofit Service、api-inventory 的 callers 指向它；规格把行为、端点写成「归某 feature」或按模块、名称关键词分桶写 page_id ownership，目标 feature 的 AC 和服务层里却没有它们

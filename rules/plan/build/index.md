# 构建与编译

派工里写了禁止 worker 编译、不跑 hvigor、附 ArkTS 限制清单，或者交回的报告、回执、CHECK-1、编译门报告里写了构建结果（BUILD SUCCESSFUL / FAILED、0 errors、编译尚未执行）时

## 触发族

- [交回报告里的构建结果](build-result-claims/index.md)（4 条）：收尾报告、验收报告或回执写「最终构建通过」「ArkTS 0 errors」「编译尚未执行」，引用的 BUILD SUCCESSFUL 早于最后一次源码写入、复核构建还没结果，或批量横切改动后构建中止就停了
- [禁止 worker 编译时附的 ArkTS 限制清单](arkts-restrictions/index.md)（1 条）：修复任务要向系统 API 传观察者或回调对象（如 errorManager.on('error', ...)），派工写「不跑 hvigor」，附的 ArkTS 限制清单里没有 arkts-implements-only-iface
- [返修派工里转述的上游禁令](rework-restrictions/index.md)（1 条）：上游规则原文带替代写法（如「No Record<K,V> indexed signatures — use explicit typed fields or HashMap」），派给 worker 的限制只剩「No Record<K,V>」，要求「Do not run the full build」却没写汇总后的全量构建
- [编译修复改动的 stateStyles / @Styles 写法](dsl-compile-fix/index.md)（1 条）：编译修复改了 .stateStyles 或 @Styles 这类 d.ts 里类型是 any 的 UI DSL 写法，编译门报告对这处只写构建 PASS，没列成需打开页面验证的项
- [派工里的编译安排（禁止 worker 编译）](build-gate/index.md)（1 条）：派工说明写了禁止 worker 自行编译（「Do NOT run hvigor builds」「由主线程做最终构建」），却没要求对照导入名与导出名，也没安排收报告前的编译门

# 禁止 worker 编译时附的 ArkTS 限制清单

agent 会看到什么：修复任务要向系统 API 传观察者或回调对象（如 errorManager.on('error', ...)），派工写「不跑 hvigor」，附的 ArkTS 限制清单里没有 arkts-implements-only-iface

## 规矩

- rule-1ec105d27f67｜派工禁止 worker 编译时，ArkTS 限制清单列上 implements-only-iface 这类规则｜读到：修复任务要向系统 API 传观察者或回调对象（如 errorManager.on('error', ...)）；写错：派工写「不跑 hvigor，由主线程统一编译」，附的 ArkTS 限制清单只有无 Record、无 in、无 any 等，没有 arkts-implements-only-iface

# 吐司与通知

审计或计划里有直接 Toast 统一成 ToastService、调用数归零的横切行，或者把 Notification 整体推迟时

## 触发族

- [计划里的吐司统一和通知推迟](toast-notification/index.md)（3 条）：审计或计划里有「直接 Toast → 统一 ToastService → 调用数归零」的横切行，或把 Notification 整体推迟，计划和批次检查项没有落到产出批次、计数和数据的承接方式

# APPROXIMATELY_LOCATION 与 LOCATION 成组声明、申请与判定：要精确定位也两项同申，任一授予就继续定位

ID：`lesson-b72e0d67fe27db2ae041` · 版本：3 · 阶段：execute · 主题：[app/map](index.md)

概要：精确与模糊定位权限成组声明申请，任一授予即继续定位

信号：`ohos.permission.APPROXIMATELY_LOCATION`, `ohos.permission.LOCATION`, `ACCESS_FINE_LOCATION`, `ACCESS_COARSE_LOCATION`, `requestPermissionsFromUser`, `authResults`, `requestPermissions`

## 何时使用

定位能力实现阶段，编写定位权限的 module.json5 声明、运行期申请与申请结果判定时

## 适用情境

目标同时申请 ohos.permission.APPROXIMATELY_LOCATION 与 ohos.permission.LOCATION；工程 skill 提供通用的权限辅助模板（遍历 authResults，任一不为 0 即返回失败）；功能规格只要求两项权限都声明、都处理。源端以 ACCESS_FINE_LOCATION 与 ACCESS_COARSE_LOCATION 一起请求；工程的通用权限表可能只列了 ohos.permission.LOCATION。

## 原因

用户可以只授予模糊位置，此时精确权限为拒绝；按“全部授予”判定会把这种情况当成无权限，定位按钮直接失败。来源中实现者照搬通用模板写出全部授予的循环，skill 与规格都没有说明定位权限组可以只授予模糊位置。另一应用中，实现者把源端的精确+模糊两项压成只申请 LOCATION，module.json5 也只声明这一项，系统判定不需要弹窗，定位入口没有授权弹窗；规格指向的核验 skill 写明 LOCATION 不能单独申请，实现者没有读它，只参考了通用权限表。

## 做法

1. authResults 中任一定位权限授予（至少模糊位置为 0）就继续定位；只有精确权限缺失时按降级精度处理，两项都拒绝才走失败提示。
2. Android 的 ACCESS_FINE_LOCATION + ACCESS_COARSE_LOCATION 映射为 LOCATION + APPROXIMATELY_LOCATION：需要精确定位时，module.json5 的 requestPermissions 与 requestPermissionsFromUser 的列表都同时包含两项，LOCATION 不单独申请；调用定位 API 前查 d.ts 的 @permission 注解，不以通用常用权限表代替。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [PowerShell 读文件带 UTF8 编码，乱码视为未读](../../process/unloaded-input/lesson-6a3a7f46c8fec282affa.lesson.md)（共享 1 张卡）
- [编译按完整 ERROR 列表判定，失败只记 FAIL](../../process/claimed-without-receipt/lesson-7426a20525e52e34c2e7.lesson.md)（共享 1 张卡）
- [规格与源码冲突按源实现，例外只认决策 ID](../../process/secondary-over-source/lesson-7a065e8fe384b8c462cc.lesson.md)（共享 1 张卡）
- [异步结果回调按成功失败分支列全副作用逐项对齐](../../ui/state/feedback/lesson-ac7a2e17b8d88c3cee7b.lesson.md)（共享 1 张卡）
- [占位地图换原生地图时接定位出口并转换坐标系](lesson-b5e8609c6602b3828fa9.lesson.md)（共享 1 张卡）

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-8c249997059a2524ea7b](../../../../store/cases/case-8c249997059a2524ea7b/921750461c1e7e278c419ca26c21b17048d692c94b180c54164c66f94aafa6e6.json) · 结论：diagnosis, rec-114085c20a, rec-cf452dc744
  卡片版本：`921750461c1e7e278c419ca26c21b17048d692c94b180c54164c66f94aafa6e6`
- [case-f9c6cd0dc22c13bdcdd8](../../../../store/cases/case-f9c6cd0dc22c13bdcdd8/49829f5fdc419a33101e6e6ef4b3c0cc17771d6649145267def11b9498e45dfc.json) · 结论：diagnosis, rec-31b0843fb8
  卡片版本：`49829f5fdc419a33101e6e6ef4b3c0cc17771d6649145267def11b9498e45dfc`

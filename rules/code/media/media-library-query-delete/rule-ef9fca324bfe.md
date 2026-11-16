# 删除取消的测试替身用设备实测的 201 + 'user deny'，取消和失败分开断言

审的是：代码
触发（任一种）：
- 读到：已有回归测试里 `rejected or cancelled` 删除用例断言不提示、保留当前缩略图和持久目标；写错的样子：测试把取消假定成 `14000011` 之类没核实的码并期望失败提示，或者把 `rejected or cancelled` 用例的期望从无提示改成失败提示
适用范围：给带系统确认框的删除接口写或改测试替身和断言时
做法：
- 把「rejected or cancelled」拆成取消与失败两个用例：取消只记日志、不提示、不清除媒体记录；只有真正失败才断言失败或权限提示
- 替身里取消写成异步拒绝 { code: 201, message: 'user deny' }，另分别覆盖同步异常、权限申请失败和确认框取消；不用假定的 14000011 代表取消
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 确认框点取消：Promise 异步拒绝，code 201、message 'user deny'：设备实测的取消返回，替身照这个写（出处：卡里修好并验证过）
- 14000011 - System inner fail：声明里 14000011 是系统内部失败，不是取消（出处：鸿蒙 SDK 的 ets/api/@ohos.file.photoAccessHelper.d.ts，MediaAssetChangeRequest.deleteAssets）
未核实：'user deny' 是否稳定契约，卡里也没核到
来源：1 张卡，1 个应用
- case-cd4f1c37e7e321bb50d6（opencamera-hmos）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 3、诊断；取值 1 ← 诊断

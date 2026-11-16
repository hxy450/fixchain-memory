# catch 里重新抛出时先收窄成 Error，不直接 throw catch 变量

审的是：代码
触发（任一种）：
- 读到：规格或巡检要求区分「过期任务的异常按取消处理、当前任务的异常继续上报」，由上层处理返回的 Promise，需要在 catch 分支里有条件地向上抛；写错的样子：ArkTS 代码里写出 `catch (error) { … throw error; }`，把未定类型的 catch 变量原样抛出；编译报 10605087 `arkts-limited-throw`
适用范围：ArkTS 严格模式工程里，catch 分支把捕获到的异常继续向上抛出时
做法：
- 写成 throw error instanceof Error ? error : new Error(String(error))，或抛出携带原因的新 Error
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- ArkTS 只支持抛出 Error 类或其派生类的实例（规则 arkts-limited-throw，错误码 10605087）：catch 变量类型未定，不能直接抛（出处：typescript-to-arkts-migration-guide.md，限制throw语句中表达式的类型）
- throw error instanceof Error ? error : new Error(String(error));：改后复编通过的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-7da8b355891030ab0ada（听音练习）：做法第 1 步 ← 建议 1、诊断；取值 2 ← 诊断

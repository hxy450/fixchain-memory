# 写 push/replace 时，目的地源 Activity 关了进入转场就传第三参数 false

审的是：代码
触发（任一种）：
- 读到：目的地源 Activity 或其基类 onCreate 有 overridePendingTransition(0, 0)；工程里已有路由调用传了 false；写错的样子：navPathStack.pushPathByName(name, param) / replacePathByName(name, param) 只写两个参数，进入该页带系统转场动画
适用范围：目标代码用 NavPathStack 进入某页、源端该 Activity 关闭了进入转场时
做法：
- 核对目的地源 Activity（含基类）是否关闭进入转场；关了就写成 pushPathByName(name, param, false) / replacePathByName(name, param, false)
- 与工程已有路由的写法保持一致；规格只给两参伪代码时，不据此省略第三参数
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- pushPathByName(name: string, param: unknown, animated?: boolean): void，animated 默认 true：进入页面，false 表示无转场（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.pushPathByName）
- replacePathByName(name: string, param: Object, animated?: boolean): void，animated 默认 true：替换栈顶页，false 表示无转场（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.replacePathByName）
- pushPath(info: NavPathInfo, animated?: boolean): void：同族接口：NavPathStack 按 NavPathInfo 进入（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.pushPath）
- pushDestinationByName(name: string, param: Object, animated?: boolean): Promise<void>：同族接口：NavPathStack 带结果的按名进入（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.pushDestinationByName）
- replacePath(info: NavPathInfo, animated?: boolean): void：同族接口：NavPathStack 按 NavPathInfo 替换（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.replacePath）
- 两处补第三参数 false 后，进入该页没有滑入中间帧：修法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-ab2bd55b44e47971676a（Privacy Friendly 2048）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3；取值 6 ← 诊断

# 源 Activity 或基类 onCreate 关进入转场时，规格记成目的地属性并写进每条路由契约

审的是：规格
触发（任一种）：
- 读到：源 Activity 或它继承的基类在 onCreate 里调 overridePendingTransition(0, 0)；写错的样子：规格只把转场禁用挂在抽屉基座的 AC 上，或只记了本类 onCreate 调用的那几页；进入该页的路由契约写成 pushPathByName / replacePathByName 两参，没有 animated=false，目的地页规格也没写「进入无转场」
适用范围：规格提取时，写页面规格和进入各页的路由契约伪代码
做法：
- 对每个目的地 Activity 查它及所继承基类的 onCreate（grep overridePendingTransition 和 extends）
- 命中时在该页页面规格写「进入无转场」，并在所有进入该页的路由契约（按钮跳转、教程完成、启动分流、抽屉）里写 pushPathByName(name, param, false) / replacePathByName(name, param, false)，或要求目的地页统一关闭系统转场
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- overridePendingTransition(int enterAnim, int exitAnim)：enterAnim 为 0 表示进入无动画：源端「进入该页无转场」的依据（出处：android.app.Activity#overridePendingTransition）
- pushPathByName(name: string, param: unknown, animated?: boolean): void，animated 默认 true：不写第三参数就有转场动画（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.pushPathByName）
- replacePathByName(name: string, param: Object, animated?: boolean): void，animated 默认 true：替换栈顶页同样默认有转场（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.replacePathByName）
来源：1 张卡，1 个应用
- case-ab2bd55b44e47971676a（Privacy Friendly 2048）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 1

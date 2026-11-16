# 资源有横屏覆盖时，几何代码在重算入口里运行期读资源，不用写死的常量

审的是：代码
触发（任一种）：
- 读到：源码 getResources().getInteger(R.integer.x) 读的资源在 res/values-land 有覆盖；或工程里同时有同名的常量和需要 context 的资源读取函数；写错的样子：目标几何计算直接引用写死竖屏值的 export const 常量，没有调用 resourceManager 或现有的按 context 读取的函数
适用范围：目标页面支持横竖屏、旋转后重新计算几何，所用资源随方向取不同值时
做法：
- 在旋转后重算几何的入口里按当前方向读取资源值，工程已有带 context 参数的读取函数时调用它，几何里各处改用读出的值
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- getNumber(resId: number): number：ResourceManager 运行期按资源 ID 读 integer/float 资源，结果随当前设备状态匹配的限定词目录（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，ResourceManager.getNumber）
- getNumber(resource: Resource): number（@deprecated since 20，@useinstead ohos.resourceManager.getNumber）：同族接口：按 Resource 对象读，已废弃（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，ResourceManager.getNumber）
- getNumberByName(resName: string): number：同族接口：按资源名读（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，ResourceManager.getNumberByName）
- 系统按当前设备状态先从匹配的限定词目录找资源，找不到才去 base；横屏限定词是 horizontal：目标资源 base 与 horizontal 各放一个值，运行期读取才会随方向变（出处：resource-categories-and-access.md，资源匹配）
- 重算入口里调用按 context 读取的函数取当前方向的值，横屏下几何与安卓一致：返修后的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-671195967d859fca683d（Blockinger）：做法第 1 步 ← 诊断、建议 2；取值 5 ← 诊断

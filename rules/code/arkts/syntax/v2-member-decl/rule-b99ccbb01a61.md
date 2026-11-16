# 自定义组件的 @Param / @Local / 私有成员不与 width、position 等通用属性同名

审的是：代码
触发（任一种）：
- 读到：调用点按 `({ width: …, height: … })` 给新组件传尺寸；工程已有的 Lottie 组件把实例存为 animationItem；写错的样子：组件里声明 @Param width / @Param height，或 private animation: AnimationItem | undefined
- 读到：规格的「@Local 变量」状态接口表或源端字段里有 position、width、id 等名字；写错的样子：struct 里写出 @Local position: number 这类与通用属性同名的成员；编译报 Type 'number' is not assignable to type '(value: Position | Edges | LocalizedEdges) => CommonAttribute'
适用范围：新写自定义组件 struct（不只页面）、声明 @Param、@Local、@Event 或私有字段时，规格已给出成员名也照查
做法：
- 声明前对照 CommonMethod 的方法名（width、height、position、id、animation、onClick、visibility、zIndex 等），同名即改名（尺寸参数改 contentWidth / contentHeight，position → playbackPosition，Lottie 实例用 animationItem），调用点和引用处一并改
- 先写调用点、替别的组件约定参数名时同样避开这些名字
- 规格给的名字冲突时照样改名，并在转换报告里写明改后的名字，回写规格
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- declare class BaseCustomComponent extends CommonAttribute；declare class CommonAttribute extends CommonMethod<CommonAttribute>：自定义组件继承了全部通用属性方法，同名成员会和它们冲突（出处：鸿蒙 SDK 的 ets/component/common.d.ts，BaseCustomComponent、CommonAttribute）
- declare class CustomComponentV2 extends BaseCustomComponent：@ComponentV2 组件的基类，同样带通用属性（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CustomComponentV2）
- width(value: Length): T；height(value: Length): T；animation(value: AnimateParam): T：卡里撞名的三个通用属性方法（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.width / CommonMethod.height / CommonMethod.animation）
- position(value: Position | Edges | LocalizedEdges): T：同名成员会和这个方法冲突，报错里的类型就是它（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.position）
- 编译报 animation / width / height 不能赋给 CustomComponent 同名属性；改名为 animationItem、contentWidth / contentHeight 并同步调用点后通过：修好后的写法（出处：卡里修好并验证过）
未核实：一张卡（case-5f5a856b7e04d91c8df6）的编译报错出自 API 26（target_sdk 26.0.0），本机核对用的是 API 23
来源：2 张卡，2 个应用
- case-5f5a856b7e04d91c8df6（组件岛Widget Island）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；取值 5 ← 诊断
- case-d33b282e5bf383e03328（AntennaPod）：做法第 1 步 ← 建议 4、诊断；做法第 3 步 ← 建议 4

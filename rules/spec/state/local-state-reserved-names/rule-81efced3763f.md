# 规格的「@Local 变量」表里成员名与 position 等通用属性同名时改名，并写出与源字段的对应

审的是：规格
触发（任一种）：
- 读到：源端事件或模型字段叫 position、duration 之类（如播放进度事件的 position），要转成组件状态；写错的样子：规格「@Local 变量」状态接口表直接沿用源字段名，写出 position / width / height / id / visibility / enabled / zIndex / opacity 这类与通用属性同名的成员
适用范围：规格里为自定义组件填状态接口表（@Local / @Param / @Event 成员名）时
做法：
- 把源字段名转成成员名前对照通用属性清单（position / width / height / id / visibility / enabled / zIndex / opacity 等），同名即改（如 position → playbackPosition），表里写出「成员名 ← 源字段」的对应
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- declare class BaseCustomComponent extends CommonAttribute：自定义组件继承了全部通用属性方法，成员不能和它们同名（出处：鸿蒙 SDK 的 ets/component/common.d.ts，BaseCustomComponent）
- position(value: Position | Edges | LocalizedEdges): T；width(value: Length): T；height(value: Length): T；id(value: string): T；visibility(value: Visibility): T；enabled(value: boolean): T；zIndex(value: number): T；opacity(value: number | Resource): T：清单里各名字在 CommonMethod 上的签名（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.position 等）
来源：1 张卡，1 个应用
- case-d33b282e5bf383e03328（AntennaPod）：做法第 1 步 ← 建议 3、诊断

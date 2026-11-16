# 拆 AppStorageV2 共享 VM 改各页 new 时，跨页状态改用 @Param+@Monitor 下传

审的是：代码
触发（任一种）：
- 读到：被拆的 ViewModel 经 AppStorageV2.connect 同一个 key 由各页 getInstance() 共用；其中的 @Trace 状态字段由某一页的动作写入，其他页只读（含查询时隐式读取）；写错的样子：各调用处把 getInstance() 机械替换成 new 出来的 ViewModel 实例，读取页没有新增对应的 @Param + @Monitor，也没有订阅事件；写入动作只改了写入页自己的私有实例
适用范围：把跨页面共享的 ViewModel 单例（AppStorageV2 等全局存储）改成页面级实例的重构
做法：
- 对 VM 里每个跨页面状态字段，先列出写入它的动作和全部读取页
- 每个读取页改成显式输入：在 @ComponentV2 组件里声明该字段的 @Param，由父页传入，并用 @Monitor('该字段') 在变化时重新查询；或者订阅一个带类型的事件
- 原先写共享实例的一方（如侧栏选择弹层）删掉对自己私有 VM 的查询和写入，改成保存成功后回调通知父页，由父页更新下传的值；只刷新私有实例、无人显示的 VM 调用一并删掉
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- static connect<T extends object>(type: TypeConstructorWithArgs<T>, keyOrDefaultCreator?: string | StorageDefaultCreator<T>, defaultCreator?: StorageDefaultCreator<T>): T | undefined：同一个 key 已有值时返回已有对象，所以各页 connect 同一 key 拿到的是同一个实例，这就是被拆掉的隐式通道（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.StateManagement.d.ts，AppStorageV2.connect）
- @Param：由父到子单向同步，组件内不能本地修改；数据源是 @Local 或 @Param 时变化会同步给子组件：读取页用 @Param 接收父页的状态，改动要由父页的数据源发起（出处：arkts-new-param.md，装饰器说明、变量传递）
- declare type MonitorDecorator = (value: string, ...args: string[]) => MethodDecorator：@Monitor 的参数是要监听的属性路径，可写多个（出处：鸿蒙 SDK 的 ets/component/common.d.ts，MonitorDecorator）
- @Monitor 只能监听被 @Local、@Param、@Provider、@Consumer、@Computed 装饰的变量：读取页要先把字段声明成 @Param，@Monitor 才能收到变化（出处：arkts-new-monitor.md，监听变化）
来源：1 张卡，1 个应用
- case-8f714106a538afa3c22a（记得日历）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断；做法第 3 步 ← 诊断

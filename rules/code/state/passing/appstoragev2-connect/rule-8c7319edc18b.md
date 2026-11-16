# 模型要被其他页面读写时，页面从一开始用 AppStorageV2.connect 取共享实例，不 new 私有实例

审的是：代码
触发（任一种）：
- 读到：规格或决策写某个模型要被其他功能或页面读写（如「向 F003 提供候选数据」）；写错的样子：页面里 `@Local model = new …(...)` 自己创建私有实例，另一个页面用 AppStorageV2.connect 取到的是另一份
适用范围：Navigation 下多个页面共享同一个 @ObservedV2 模型时
做法：
- 各页面都写 @Local model: 模型类 = AppStorageV2.connect(模型类, '<同一个 key>', () => new 模型类())!，不在页面里 new 私有实例
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- static connect<T extends object>(type: TypeConstructorWithArgs<T>, keyOrDefaultCreator?: string | StorageDefaultCreator<T>, defaultCreator?: StorageDefaultCreator<T>): T | undefined：key 已有值就返回它，没有就用 defaultCreator 创建并返回；@since 12（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.StateManagement.d.ts，AppStorageV2.connect）
- 同一个 key，connect 不同类型的数据会导致应用异常：各页面 connect 时类型和 key 要一致（出处：arkts-new-appstoragev2.md，使用说明）
- static connect<T extends object>(type: TypeConstructorWithArgs<T>, keyOrDefaultCreator?: string | StorageDefaultCreator<T>, defaultCreator?: StorageDefaultCreator<T>): T | undefined（PersistenceV2 extends AppStorageV2）：同族接口：PersistenceV2 继承同一个 connect，需要持久化时用它（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.StateManagement.d.ts，PersistenceV2）
来源：1 张卡，1 个应用
- case-fa7ad75016781faf0cc5（听音练习）：做法第 1 步 ← 建议 2、诊断

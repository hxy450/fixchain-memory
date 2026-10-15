# 源端初始化本就同步时目标也同步执行（用 Sync 接口、不加输入门控）；确需异步时，用户可编辑的输入状态在第一个 await 之前写入初值

ID：`lesson-843a70afd7e08bfed97c` · 版本：5

[本主题](index.md)

## 何时使用

页面、自绘组件或 ViewModel 实现阶段，把源端构造器或 onCreate 中的初始化移到目标生命周期回调、决定是否异步，并编排异步步骤与输入状态初值的先后时

## 适用情境

源端在 Activity.onCreate 或自定义 View 构造器里同步完成初始化（取尺寸、解码位图、建局面、写入关键词或输入框文本）后才接收输入；目标准备在 aboutToAppear 等生命周期回调里调用不被等待的 async 方法（异步解码、存储、SDK 绑定），可能用 try/catch 只记日志，或以 booted/ready 标志忽略初始化完成前的输入；输入框双向绑定 ViewModel 字段。

## 原因

页面不等初始化完成就可编辑；续体里较晚到达的初值赋值会覆盖用户已输入的文字，点击操作可能读到空值。在 await 链前再插入异步步骤，会把初值进一步推迟。生命周期回调里不被等待的 async 函数抛出的异常变成被拒绝的 Promise，不再沿回调同步抛出；再包一层只记日志的 catch，源端会崩溃的路径就成了空白页面，ready 标志永不置位，输入全被丢弃。

## 做法

1. 先看源端初始化是否在构造器或 onCreate 里同步做完。是就在目标生命周期回调里按源顺序同步执行：SDK 同时有 Promise 与 Sync 变体时用 Sync 变体（例：@ohos.multimedia.image.d.ts 的 ImageSource.createPixelMapSync、@ohos.resourceManager.d.ts 的 getMediaContentSync、@ohos.window.d.ts 的 WindowStage.getMainWindowSync），不引入异步窗口，也不加源端没有的“初始化完成前忽略输入”门控；规格要求照搬的异常在这条调用链上不加 try/catch 或 Promise.catch。
2. 确需异步时，把源端同步设置的输入类状态（关键词、输入框文本、清除按钮可见性）放在第一个 await 之前赋值；异步步骤只加载数据，不在续体里回写用户可编辑字段。
3. 确需在续体赋值时，先确认用户没有编辑过该字段：一般比较字段是否仍是进入时的值即可；契约要求区分“用户改过又改回”时，改用编辑标记或版本号判断（条件推理，来源案例未单独复现该竞态）。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-7b90b1ebaae140988b90](../../../store/cases/case-7b90b1ebaae140988b90/30d01989c7dc2ab2b6f917df7ad2afba49c66c5d0889f6324c8ad9ba83ad6544.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`30d01989c7dc2ab2b6f917df7ad2afba49c66c5d0889f6324c8ad9ba83ad6544`
- [case-bc452cbde49f74ef19a3](../../../store/cases/case-bc452cbde49f74ef19a3/356f44bb0d18710202e08df16ee23f96071833deedaa6a4599dce9af2f5d2086.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:4
  卡片版本：`356f44bb0d18710202e08df16ee23f96071833deedaa6a4599dce9af2f5d2086`

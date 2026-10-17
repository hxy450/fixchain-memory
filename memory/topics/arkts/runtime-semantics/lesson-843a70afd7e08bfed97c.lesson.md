# 异步初始化里，用户可编辑的输入状态在第一个 await 之前写入初值；源端初始化本是同步的就保持同步，不加输入门控、不吞异常

ID：`lesson-843a70afd7e08bfed97c` · 版本：3 · 阶段：execute · 主题：[arkts/runtime-semantics](index.md)

概要：输入初值先于首个 await；源端同步初始化保持同步

信号：`TextInput`, `aboutToAppear`, `@Local`, `onCreate`, `createPixelMapSync`, `getMediaContentSync`, `getMainWindowSync`

## 何时使用

ViewModel 实现阶段，编排页面初始化方法中异步存储/SDK 绑定与输入状态初值的先后顺序时；切片实现阶段把源端构造器或 onCreate 里的同步初始化（取尺寸、解码位图、开局）移到组件生命周期，决定是否异步、怎样处理异常时

## 适用情境

源页面在初始化时同步写入关键词或输入框文本，操作读取实时输入；目标输入框双向绑定 ViewModel 字段，初始化方法内含 await（存储、历史、SDK 绑定），页面生命周期回调以不等待的方式调用它。 也包括源端在 Activity.onCreate 或自定义 View 构造器里同步完成取尺寸、初始化与位图解码，之后才接收输入，其中一条路径是规格要求照搬的未捕获异常崩溃；目标 SDK 对这些步骤同时提供 Promise 与 Sync 接口，写者准备在 aboutToAppear 里调用不等待的 async 启动函数、catch 只记日志，并用 booted/ready 标志拦截输入。

## 原因

页面不等初始化完成就可编辑；续体里较晚到达的初值赋值会覆盖用户已输入的文字，点击操作读到空值，表现为“点了没反应”。来源中写者读到源端先同步设置关键词与输入框，却把赋值放到 await 绑定之后；后续写者又在 await 链前插入更多异步步骤，顺序一直保留到返修。 把同步初始化改成生命周期回调里不等待的 async 函数后，其中抛出的异常变成被拒绝的 Promise，不再沿回调同步抛出；再包一层只写日志的 catch，源端会崩溃退出的路径就变成停在空白画面，ready 标志永不置位，输入全被丢弃。源端没有丢弃输入的行为，这种门控只是把异步窗口藏起来。

## 做法

1. 把源端同步设置的输入类状态（关键词、输入框文本、清除按钮可见性）放在第一个 await 之前赋值；异步步骤只加载数据，不在续体里回写用户可编辑字段。 先看源端初始化是否在构造器或 onCreate 里同步做完、之后才接收输入：是的话目标在生命周期回调（如 aboutToAppear）里按源顺序同步执行，SDK 同时有 Promise 与 Sync 变体时用 Sync 变体（写前在同一 interface 的 d.ts 里查，如 ImageSource.createPixelMapSync、resourceManager.getMediaContentSync、WindowStage.getMainWindowSync），不引入异步窗口，也不加“初始化完成前忽略输入”的门控。源端本来会抛出的异常（规格照搬的崩溃），从抛出函数到生命周期入口都不加 try/catch、Promise.catch，也不放进不被等待的 async 包装。
2. 确需在续体赋值时，先确认字段仍是进入时的值再写。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-7b90b1ebaae140988b90](../../../../store/cases/case-7b90b1ebaae140988b90/30d01989c7dc2ab2b6f917df7ad2afba49c66c5d0889f6324c8ad9ba83ad6544.json) · 结论：diagnosis, rec-88dea8e372, rec-e4f0dda00e
  卡片版本：`30d01989c7dc2ab2b6f917df7ad2afba49c66c5d0889f6324c8ad9ba83ad6544`
- [case-bc452cbde49f74ef19a3](../../../../store/cases/case-bc452cbde49f74ef19a3/356f44bb0d18710202e08df16ee23f96071833deedaa6a4599dce9af2f5d2086.json) · 结论：diagnosis, rec-44dca2125f, rec-cd5f201aea, rec-79a5f36656
  卡片版本：`356f44bb0d18710202e08df16ee23f96071833deedaa6a4599dce9af2f5d2086`

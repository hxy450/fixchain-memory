# 源端访问解包后对象的字段时，先确定目标 res.data 对应哪一层类型，再逐层写取值键

ID：`lesson-dc5c370e370c2be803c1` · 版本：2

[本主题](index.md)

## 何时使用

数据层服务实现阶段，把源端 Retrofit/Gson 响应 Bean 的字段访问路径翻译成目标端对原始 JSON 的逐键取值时；页面回调依赖服务层解析产出的 success、errorCode 等字段，准备给出“逐行一致”的复核结论时

## 适用情境

源端 success 回调已把 BaseResponse<T> 解包成 T，业务代码写 result.data?.xxx；T 本身是含 data 字段的容器 Bean（如 {total, data:{…}}）；目标网络层把响应 data 原样返回，服务层用 getObject/getArray 按键手动取值。

## 原因

源端表达式里的 result 已是解包后的容器对象，它的 .data 是容器内层；目标 res.data 指向容器对象本身。照抄表面路径 res.data.xxx 会少取一层，取值落空时常回落为空数组或默认值而不报错，页面表现为既无数据也无空态。来源中写者读到了 Bean 定义并在笔记里复述了两层结构，同一服务的其他端点也正确取了内层，只有这一端点照抄了源端路径。另一应用中两轮复核都没打开服务层解析函数，success 取信封层、errorCode 读 root 层，与源端的 data 层不符，页面分支随之错位。

## 做法

1. 写取值前先写出“目标 res.data = 源端哪一个类型”，再按该类型的字段链逐层取值：容器 Bean 含内层 data 时，先 getObject(res.data, 'data') 再取内层字段。
2. 同一服务写完多个容器端点后，逐个列出“目标取值键链 ↔ Bean 字段链”，确认层数一致。
3. 页面回调依赖服务层解析函数产出的 success、errorCode 等字段时，同时打开解析函数，核对每个字段的读取层级（信封层还是 data 层）与缺省值，再给出对齐结论。

## 可选检查

- 决定后续页面是否创建的解析结果（如分类 Tab）用一次真实响应或样例确认非空，并区分“服务端返回空”与“取值路径未命中”。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-18365c67d94d72d8a825](../../../store/cases/case-18365c67d94d72d8a825/373986a1238f539d399390372bcd09d27fa876d8acb70d6604e9722c9b467222.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`373986a1238f539d399390372bcd09d27fa876d8acb70d6604e9722c9b467222`
- [case-5b91aeeca2e493368af0](../../../store/cases/case-5b91aeeca2e493368af0/aa54f204a016acd3439a94d5a9cb4dfb52ccbcb0c6243e2813b4e1604e6dfe92.json) · 结论：diagnosis, recommendation:3
  卡片版本：`aa54f204a016acd3439a94d5a9cb4dfb52ccbcb0c6243e2813b4e1604e6dfe92`

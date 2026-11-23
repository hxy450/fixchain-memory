# 源端访问解包后对象的字段时，先确定目标 res.data 对应哪一层类型，再逐层写取值键

## 何时使用

数据层服务实现阶段，把源端 Retrofit/Gson 响应 Bean 的字段访问路径翻译成目标端对原始 JSON 的逐键取值时；页面回调依赖服务层解析产出的 success、errorCode 等字段，准备给出“逐行一致”的复核结论时

## 适用情境

源端 success 回调已把 BaseResponse<T> 解包成 T，业务代码写 result.data?.xxx；T 本身是含 data 字段的容器 Bean（如 {total, data:{…}}）；目标网络层把响应 data 原样返回，服务层用 getObject/getArray 按键手动取值。

## 例外与边界

- 少一层只发生在源端回调已把信封解包、且 T 自身又含 data 字段时；源端回调拿到的是未解包的信封（result 就是 BaseResponse<T>）时，result.data.xxx 和目标 res.data.xxx 是同一层，照原路径取值，不要再多加一层 getObject(…, 'data')。

## 原因

源端表达式里的 result 已是解包后的容器对象，它的 .data 是容器内层；目标 res.data 指向容器对象本身。照抄表面路径 res.data.xxx 会少取一层，取值落空时常回落为空数组或默认值而不报错，页面表现为既无数据也无空态。来源中写者读到了 Bean 定义并在笔记里复述了两层结构，同一服务的其他端点也正确取了内层，只有这一端点照抄了源端路径。另一应用中两轮复核都没打开服务层解析函数，success 取信封层、errorCode 读 root 层，与源端的 data 层不符，页面分支随之错位。

## 做法

1. 写取值前先写出“目标 res.data = 源端哪一个类型”，再按该类型的字段链逐层取值：容器 Bean 含内层 data 时，先 getObject(res.data, 'data') 再取内层字段。
2. 同一服务写完多个容器端点后，逐个列出“目标取值键链 ↔ Bean 字段链”，确认层数一致。
3. 页面回调依赖服务层解析函数产出的 success、errorCode 等字段时，同时打开解析函数，核对每个字段的读取层级（信封层还是 data 层）与缺省值，再给出对齐结论。

## 可选检查

- 决定后续页面是否创建的解析结果（如分类 Tab）用一次真实响应或样例确认非空，并区分“服务端返回空”与“取值路径未命中”。

来源支持：3 张卡 · 3 次迁移 · 3 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码；com.google.code.gson:gson 2.8.9、2.11.0。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕Gson 反序列化时，带 @SerializedName("x") 的字段只从 JSON 键 x 取值，和 Java 字段同名的键被忽略
- 〔做法第 3 步〕实体类没有给字段另设初值时，Gson 反序列化中 JSON 里缺失的字段保持 Java 默认值：int 为 0，boolean 为 false，引用类型为 null
- 〔做法第 3 步〕安卓 org.json 的 JSONObject.optInt(name) 在键缺失或无法转成 int 时返回 0，optBoolean(name) 返回 false

# 别的规格或契约里定义、留给本文档承接的条目

agent 会看到什么：读到共享谓词的完整条件只写在别的规格的 AC 里、跨模块契约把某个 seam 标「待 Feature Spec」、AC 范围疑似归属别的功能；交回的消费页规格、feature spec 或 UT 设计只写了名字或笼统说法，或按字面写成 RED 用例

## 规矩

- rule-77e298b4953c｜消费页规格引用源端共享谓词时，内联完整条件或指向定义它的 AC｜读到：源端多个页面共用一个判定谓词（如列表项是否在播），它的完整条件只在某一份规格的 AC 里写过；写错：消费页的规格只写了谓词的函数名，没写它的完整条件，也没指向定义它的 AC
- rule-c28db66d8e79｜契约把桥接 seam 标「待 Feature Spec」时，规格写明通道机制、通道名、事件清单和 Model 字段｜读到：跨模块契约把某个原生↔Flutter 桥接 seam 标成「待 Feature Spec」；源端宿主用 flutter_boost 的 `addEventListener` / `sendEventToFlutter` 通信；写错：feature spec 只写「EventHub 事件常量｜事件名对齐某个 MethodChannel 桥」一类笼统说法，没写通道机制、通道名、事件清单、宿主锚点和 Model 字段；或真值锚点指向了另一个 Fragment
- rule-86e7b3d10894｜AC 与实现冲突又怀疑归属别的功能时，UT 设计先查源端写入点，查不清记为 spec 待确认，不写 RED｜读到：AC 文字要求的范围比实现和源锚点大，设计者自己注了「需补方法或确认归属其他 feature」；写错：UT 设计按 AC 字面写出要求当前方法实现的 RED 用例，没有核实源端写入点和其他功能的规格

# 契约把桥接 seam 标「待 Feature Spec」时，规格写明通道机制、通道名、事件清单和 Model 字段

审的是：规格
触发（任一种）：
- 读到：跨模块契约把某个原生↔Flutter 桥接 seam 标成「待 Feature Spec」；源端宿主用 flutter_boost 的 `addEventListener` / `sendEventToFlutter` 通信；写错的样子：feature spec 只写「EventHub 事件常量｜事件名对齐某个 MethodChannel 桥」一类笼统说法，没写通道机制、通道名、事件清单、宿主锚点和 Model 字段；或真值锚点指向了另一个 Fragment
适用范围：规格提取阶段处理契约里标为「待 Feature Spec」的原生↔Flutter 桥接项时
做法：
- 读源端实现，在 feature spec 里写明：通道机制（flutter_boost 事件通道还是 MethodChannel）、通道名、事件清单（每个事件名及参数）、宿主锚点（宿主实际挂载的容器子类）、数据 Model 字段
针对本应用要查的：
- 桥接 seam 的通道机制和事件清单：源工程里宿主挂载的容器子类、事件常量文件和 Flutter 端 dart 监听处，按 addEventListener、sendEventToFlutter、MethodChannel 搜；分清是事件通道还是 MethodChannel，记下通道名、事件名、参数和对应的 Model 类
来源：1 张卡，1 个应用
- case-b98aad1336d85a238cd7（polypal-app-ohos）：做法第 1 步 ← 建议 5

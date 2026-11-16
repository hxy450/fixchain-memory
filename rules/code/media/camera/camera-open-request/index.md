# 相机打开回调里消费的一次性拍照请求

agent 会看到什么：读到 CameraDevice.StateCallback.onOpened 里读一次性标志、按它 postDelayed 后 takePicture，或契约写「相机打开完成回调内调用、先开后拍」、派工把这个标志通道交给别的切片；产物里在 aboutToAppear / onShown / onPageShow 里直接拍，或把标志写成常量 false 而没留注入点和 FWD-REF

## 规矩

- rule-8df4e04213a9｜一次性拍照请求在相机就绪后消费并沿用源端延时，不在 aboutToAppear / onShown 里直接拍｜读到：契约或 AC 写“相机打开完成回调内调用、先开后拍”，计划写的挂载点却是 aboutToAppear / onPageShow；写错：页面在 aboutToAppear、onShown 或 onPageShow 里消费请求，拿到后立即调用快门按钮的处理函数
- rule-852a9c538005｜入口标志归另一切片时，引擎回调留可注入的消费 hook 并登记 FWD-REF，不写常量 false｜读到：源端相机打开回调里读取一次性标志，作为参数传给后续的相机设置方法；派工或骨架说这个标志通道归另一个切片，要用 FWD-REF / HANDOFF 交接；写错：引擎回调里把源端读取写成常量 `= false` 并注释“通道归别的切片”，没有注入点，也没登记 FWD-REF 或 HANDOFF，后面的延时拍照分支成了死分支

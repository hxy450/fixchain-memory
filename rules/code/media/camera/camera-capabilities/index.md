# 相机能力位、模式和可选值

agent 会看到什么：读到 CameraCharacteristics 的能力键（SENSOR_ORIENTATION、CONTROL_AWB_AVAILABLE_MODES、INFO_SUPPORTED_HARDWARE_LEVEL）、打开相机时缓存的能力字段、带约束或过滤参数的尺寸选择；产物里能力 getter 的实现、写成常量 true 的能力位、写死的角度和模式列表

## 规矩

- rule-77119fbe4dd7｜源端相机能力 getter 读打开期缓存时，目标在会话 commit 后快照一次，getter 只读内存｜读到：源端打开相机时调一次 CameraManager#getCameraCharacteristics（或包它的能力枚举）存进字段，能力 getter 只返回这个字段；写错：目标的能力 getter 每次调用都执行 cameraManager.getSupportedOutputCapability(...) 和 session.isFocusModeSupported(...)、getExposureBiasRange() 等同步查询，只在注释里说有缓存
- rule-dd8173f93742｜源端读 SENSOR_ORIENTATION 时，目标读 cameraOrientation，不写死角度｜读到：源端用 `CameraCharacteristics.SENSOR_ORIENTATION` 的值参与预览或拍照的旋转计算；写错：目标端按前后摄写死 90 / 270，或注释写鸿蒙没有传感器角度属性；没有读 `cameraOrientation`
- rule-78a52ffec706｜相机能力位取自会话查询，不因有某枚举或 setter 就置 true｜读到：源端能力位来自 CameraCharacteristics（CONTROL_AWB_AVAILABLE_MODES、INFO_SUPPORTED_HARDWARE_LEVEL），规格给出条件式能力规则；写错：因 WhiteBalanceMode 等枚举有 LOCKED、MANUAL 或有 setWhiteBalance 就把能力位写成常量 true，色温范围写死
- rule-c756c68a70d4｜源端按硬件等级推出录像中拍照能力位时，目标按 NORMAL_VIDEO 能力和 canAddOutput 判定｜读到：源端按硬件等级（如 `LIMITED`）推出录像中拍照的能力位，录像中快照按这个能力位门控；写错：目标把这个能力位恒置 true；或录像会话里已 removeOutput 掉 photoOutput，快照门控和按钮仍按静态能力位为真
- rule-d2931c3489c6｜白平衡预设按 WhiteBalanceMode 逐个查询后暴露，解锁时恢复所选模式和色温｜读到：源端白平衡可选值来自 CONTROL_AWB_AVAILABLE_MODES（auto、cloudy-daylight、incandescent、fluorescent、daylight 等），解锁白平衡时回到用户所选的模式；写错：白平衡值只暴露 ['auto','manual']；解除白平衡锁时固定 setWhiteBalanceMode(WhiteBalanceMode.AUTO)
- rule-8840e2fa76e3｜源控制器里前屏补光分支回调 UI 时，目标控制器保留「是否需补光」查询和触发出口｜写错：目标相机控制器把前屏补光的开、自动两种模式映射成 camera.FlashMode.FLASH_MODE_CLOSE，注释写「由 UI 层承担」，却没有判定是否需要补光的查询、没有触发出口，也没有登记占位和消费方
- rule-09d8d9917b74｜源端带约束或过滤参数的尺寸选择，移植时保留参数和降档、过滤分支｜读到：源端把约束对象传进偏好读取，选尺寸时约束不满足就降到满足约束的最大尺寸；尺寸列表方法带 boolean 过滤参数（按连拍、扩展模式、约束过滤），调用方传 `(true)`；写错：目标端把约束参数传成 `null` 或改名不用（注释「constraints 未消费」），只实现保存值和最大面积两支；带过滤参数的方法改成无参、直接返回全量列表，弹出菜单的分辨率列表用了它

# 源端应用内直接开关蓝牙时，规格先查 access 声明，不把现有跳设置的实现当平台限制

审的是：规格
触发（任一种）：
- 读到：源码或可达图里点击开关直接调用 BluetoothAdapter.enable() / disable()；决策台账只允许「平台不允许应用直接完成的开关」改走系统授权弹窗或设置跳转；现有鸿蒙代码的开关是打开系统蓝牙设置；写错的样子：规格写「蓝牙开关走系统设置并在返回时回读」、验收条目写「进入系统设置并回读」，或把这条外部边归为 `PLATFORM_EQUIVALENT`，却没有引用目标 SDK 的声明说明平台不允许
适用范围：规格里为源端在应用内直接开关的系统能力（蓝牙开关等）定鸿蒙实现方式和验收项时
做法：
- 先查目标 SDK 对应模块的声明再定：蓝牙查 @ohos.bluetooth.access 里 enableBluetooth / disableBluetooth / enableBluetoothAsync / disableBluetoothAsync 的 @permission 和 @since；它们只要 ohos.permission.ACCESS_BLUETOOTH，规格写成应用内开关
- 只有声明里确实没有应用可用的接口时才写「走系统设置」，并写明依据的声明；现有实现不能当作平台限制的证据
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- function enableBluetooth(): void；function disableBluetooth(): void（@permission ohos.permission.ACCESS_BLUETOOTH）：应用内同步开关蓝牙，只要 ACCESS_BLUETOOTH（出处：鸿蒙 SDK 的 ets/api/@ohos.bluetooth.access.d.ts，access.enableBluetooth / access.disableBluetooth）
- function enableBluetoothAsync(): Promise<void>；function disableBluetoothAsync(): Promise<void>（@permission ohos.permission.ACCESS_BLUETOOTH，@since 20）：应用内开关蓝牙、弹系统确认的异步接口（出处：鸿蒙 SDK 的 ets/api/@ohos.bluetooth.access.d.ts，access.enableBluetoothAsync / access.disableBluetoothAsync）
来源：1 张卡，1 个应用
- case-fa0174cd489361d7586d（骑行记录）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1

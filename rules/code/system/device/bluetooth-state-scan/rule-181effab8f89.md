# 源端应用内开关蓝牙时，代码按 API 版本调 access 开关接口，不固定跳系统设置

审的是：代码
触发（任一种）：
- 读到：安卓点击开关时直接调用 BluetoothAdapter.enable() / disable()；写错的样子：鸿蒙服务的开、关方法固定拉起系统蓝牙设置页，没有调用 access.enableBluetoothAsync / access.enableBluetooth
适用范围：鸿蒙端实现源端应用内直接开关的蓝牙开关时
做法：
- 按运行时版本分支：deviceInfo.sdkApiVersion >= 20 时 await access.enableBluetoothAsync() / access.disableBluetoothAsync()，catch 到 BusinessError 2900013、2900014 时开关按回读状态复位；低版本走 access.enableBluetooth() / disableBluetooth() 或设置页兜底
- 开关显示以 access.getState() 和 access.on('stateChange', …) 回读为准，映射 BluetoothState 时把 STATE_BLE_ON 等 BLE 状态也覆盖到
- 规格写成跳转设置而源码是应用内开关、SDK 又有可用接口时，回报规格疑点，不照旧保留跳转
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- function enableBluetoothAsync(): Promise<void>；function disableBluetoothAsync(): Promise<void>（@since 20）：API 20+ 应用内开关蓝牙，带系统确认（出处：鸿蒙 SDK 的 ets/api/@ohos.bluetooth.access.d.ts，access.enableBluetoothAsync / access.disableBluetoothAsync）
- function enableBluetooth(): void；function disableBluetooth(): void：低版本的同步开关（出处：鸿蒙 SDK 的 ets/api/@ohos.bluetooth.access.d.ts，access.enableBluetooth / access.disableBluetooth）
- 2900013 - The user does not respond.；2900014 - User refuse the action.：异步开关要处理的两个用户错误码（出处：鸿蒙 SDK 的 ets/api/@ohos.bluetooth.access.d.ts，access.enableBluetoothAsync 的 @throws）
- const sdkApiVersion: number：运行时的 SDK API 版本号，用来做版本分支（出处：鸿蒙 SDK 的 ets/api/@ohos.deviceInfo.d.ts，deviceInfo.sdkApiVersion）
- function getState(): BluetoothState；function on(type: 'stateChange', callback: Callback<BluetoothState>): void：回读和订阅蓝牙状态（出处：鸿蒙 SDK 的 ets/api/@ohos.bluetooth.access.d.ts，access.getState / access.on('stateChange')）
- STATE_OFF = 0、STATE_TURNING_ON = 1、STATE_ON = 2、STATE_TURNING_OFF = 3、STATE_BLE_TURNING_ON = 4、STATE_BLE_ON = 5、STATE_BLE_TURNING_OFF = 6：BluetoothState 的全部取值（出处：鸿蒙 SDK 的 ets/api/@ohos.bluetooth.access.d.ts，access.BluetoothState）
- API 20+ 用异步接口应用内系统确认，保留运行时版本分支与设置页兜底，新增 STATE_BLE_ON 映射测试：修好后的实现要点（出处：卡里修好并验证过）
未核实：修复的写入不在卡的材料内，最终实现以分析推荐和构建说明为据；卡里没写版本分支用的具体判断，deviceInfo.sdkApiVersion 是按声明补的；STATE_BLE_ON 映射成开还是关卡里没写
来源：1 张卡，1 个应用
- case-fa0174cd489361d7586d（骑行记录）：做法第 1 步 ← 诊断、建议 2；做法第 2 步 ← 诊断、建议 2；做法第 3 步 ← 建议 4；取值 7 ← 诊断

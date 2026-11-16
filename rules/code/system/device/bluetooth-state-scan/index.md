# 蓝牙开关、状态和扫描

agent 会看到什么：读到源端 BluetoothAdapter（isEnabled、enable / disable、ACTION_STATE_CHANGED、startDiscovery、BluetoothDevice.getName）；产物里 @ohos.bluetooth.access / ble / connection 的开关、stateChange 回调、扫描调用和失败处理

## 规矩

- rule-4e028cad9309｜初始水合先同步读 access.getState() 通知 UI，再 await 偏好和通知授权｜读到：源端 initView 先同步读蓝牙开关设置开关图，再读偏好；写错：ViewModel 的 load() 在权限、偏好、通知授权等几次 await 之后才给开关赋值（= getState() 或 isEnabled()）
- rule-8d5b1fd98e93｜蓝牙 stateChange 回调后以 access.getState() 回读，只让终态驱动开关｜读到：源端 BroadcastReceiver 处理 BluetoothAdapter.ACTION_STATE_CHANGED，只在 STATE_ON / STATE_OFF 终态通知；写错：access.on('stateChange', state => 开关 = (state === access.BluetoothState.STATE_ON))，ViewModel 直接把回调参数写成开关真值，非 STATE_ON 一律当关闭并清空设备
- rule-181effab8f89｜源端应用内开关蓝牙时，代码按 API 版本调 access 开关接口，不固定跳系统设置｜读到：安卓点击开关时直接调用 BluetoothAdapter.enable() / disable()；写错：鸿蒙服务的开、关方法固定拉起系统蓝牙设置页，没有调用 access.enableBluetoothAsync / access.enableBluetooth
- rule-4c09fc6f3f59｜点击时实时读开关的门控放进 ViewModel：先申请权限再回读，不用 @Local 快照｜读到：源端点击入口时实时调用 isBluetoothEnabled() 一类方法读 BluetoothAdapter，关闭才提示，随后申请蓝牙权限再进设备页；写错：页面点击处理里 if (!this.bluetoothEnabled) { 提示; return }，用 @Local 快照在权限申请和实时回读之前拦截导航
- rule-721ca1aaf1de｜封装声明为 void 却带 @throws 的同步系统接口时，服务层 try/catch 收敛成返回值｜读到：鸿蒙 SDK 声明里 `startBLEScan(...)`、`stopBLEScan()` 返回 `void`，注释列有 `@throws { BusinessError } 2900003 - Bluetooth disabled.` 等错误码；写错：服务层直接调用 `ble.startBLEScan(...)` / `ble.stopBLEScan()`，外面没有 `try/catch`，调用后直接置 `scanning = true`
- rule-aff174a76aa2｜源端显式建模扫描失败和适配器关闭时，目标服务映射成可查询的错误给页面用｜读到：源端用 `BluetoothState` 一类适配器状态和 `BleScanStartException` 一类扫描启动异常建模失败，决策台账有「不崩溃、显式失败」的兜底决策；写错：目标服务的 `startScan()` 返回 `void`，不查适配器状态、不保存失败原因，页面拿不到任何失败信息
- rule-ad0f47124b84｜页面调用可能失败的服务时检查结果并复位进行中状态，规格里的失败分支逐个实现｜读到：页面规格里有失败分支，如蓝牙关闭时显示恢复卡（打开蓝牙设置），状态取自 `@ohos.bluetooth.access`；写错：页面先置 `scanning = true` 再调用服务的 `startScan()`，不检查返回值、失败不复位；没有规格里的蓝牙关闭恢复卡，只在超时后提示没找到设备
- rule-9e41919ae55d｜接入平台蓝牙设备名时在单一入口归一：空名、等于地址或 12 位十六进制都当作无名称｜读到：源端用 `BluetoothDevice.getName()` 取设备名，取不到时为 null，列表按空名回退；写错：目标端把 `connection.getRemoteDeviceName(deviceId)`、扫描结果的 `deviceName` 在各页直接拿来显示，没有在一个入口把空名、等于地址或形如 12 位十六进制的名称归一为无名称

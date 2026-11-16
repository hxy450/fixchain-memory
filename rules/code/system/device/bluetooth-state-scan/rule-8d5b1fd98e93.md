# 蓝牙 stateChange 回调后以 access.getState() 回读，只让终态驱动开关

审的是：代码
触发（任一种）：
- 读到：源端 BroadcastReceiver 处理 BluetoothAdapter.ACTION_STATE_CHANGED，只在 STATE_ON / STATE_OFF 终态通知；写错的样子：access.on('stateChange', state => 开关 = (state === access.BluetoothState.STATE_ON))，ViewModel 直接把回调参数写成开关真值，非 STATE_ON 一律当关闭并清空设备
- 读到：被替换的旧实现在状态变化时先回读 isEnabled() 再刷新；写错的样子：重写后 on('stateChange') 回调直接用回调参数写开关，回读被去掉
适用范围：用 @ohos.bluetooth.access 订阅蓝牙开关状态并驱动开关、设备入口和连接页时
做法：
- 收到回调即回读 const s = access.getState()；s 为 STATE_ON（业务需要时含 STATE_BLE_ON）即开
- 只有回读和回调都为 STATE_OFF 才报关闭；TURNING_*、BLE 过渡态和迟到回调不直接写成 false
- 重写已有状态处理前对照被替换的旧逻辑和源端广播分支；旧实现已是变化时回读、源端只处理终态时，不改成信任回调参数
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- function on(type: 'stateChange', callback: Callback<BluetoothState>): void：订阅蓝牙开关状态变化，回调带 BluetoothState（出处：鸿蒙 SDK 的 ets/api/@ohos.bluetooth.access.d.ts，access.on('stateChange')）
- function getState(): BluetoothState：同步取当前蓝牙状态；@since 13 起声明不再标 @permission（出处：鸿蒙 SDK 的 ets/api/@ohos.bluetooth.access.d.ts，access.getState）
- BluetoothState：STATE_OFF = 0、STATE_TURNING_ON = 1、STATE_ON = 2、STATE_TURNING_OFF = 3、STATE_BLE_TURNING_ON = 4、STATE_BLE_ON = 5、STATE_BLE_TURNING_OFF = 6：终态只有 STATE_ON、STATE_OFF（和 LE 模式的 STATE_BLE_ON），其余是过渡态（出处：鸿蒙 SDK 的 ets/api/@ohos.bluetooth.access.d.ts，access.BluetoothState）
- 回调改为 access.getState() 回读：ON / BLE_ON 视为开启，仅当当前状态与回调同为 STATE_OFF 才报关闭；真机回读为 STATE_ON(2)：修好的写法，迟到的 OFF 不再覆盖（出处：卡里修好并验证过）
未核实：未授予 ACCESS_BLUETOOTH 时 access.getState() 的实际表现没核实；卡里没记鸿蒙 SDK 版本，声明按本机 API 23 核实
来源：1 张卡，1 个应用
- case-c9f54856d3fb74cbd54b（骑行记录）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1、诊断；做法第 3 步 ← 建议 2；取值 4 ← 诊断

# 点击时实时读开关的门控放进 ViewModel：先申请权限再回读，不用 @Local 快照

审的是：代码
触发（任一种）：
- 读到：源端点击入口时实时调用 isBluetoothEnabled() 一类方法读 BluetoothAdapter，关闭才提示，随后申请蓝牙权限再进设备页；写错的样子：页面点击处理里 if (!this.bluetoothEnabled) { 提示; return }，用 @Local 快照在权限申请和实时回读之前拦截导航
- 读到：源端设备连接页只注册监听并 startDiscovery()，没有开关拦截；写错的样子：目标连接页的 load() 在申请权限前先按开关拦截并报蓝牙关闭
适用范围：把源端点击瞬间读取系统状态的门控（蓝牙开关等）接到页面和 ViewModel 时
做法：
- 页面把点击直接交给 ViewModel；ViewModel/Service 先完成权限申请，再实时 access.getState() 回读决定是否放行
- 目标页不新增源端没有的开关拦截
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- function getState(): BluetoothState：同步回读当前开关状态，用在决策点上（出处：鸿蒙 SDK 的 ets/api/@ohos.bluetooth.access.d.ts，access.getState）
- 移除页面本地拦截，入口交给 ViewModel 先申请权限、再实时判定开关：修好的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-c9f54856d3fb74cbd54b（骑行记录）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4、诊断；取值 2 ← 诊断

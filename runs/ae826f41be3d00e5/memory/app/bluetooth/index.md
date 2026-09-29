# app/bluetooth

蓝牙能力：适配器开关状态的真值、门控与初始加载，分协议连接状态的聚合与成功判定，应用内开关蓝牙的方式，扫描等同步接口的抛错收敛与失败态

[上一级](../index.md)

## 本级经验

- [分协议的蓝牙连接回调按设备聚合：所有协议都断开才判定设备断开，连接、配对与断开成功以回调或回读确认](lesson-ecc67592eba3402c0a1f.lesson.md)
  - 时机：实现蓝牙设备连接、断开状态与“连接/断开成功”判定时
  - 情境：源端用 ACL 等设备级广播判断连接与断开；目标用 A2DP、HFP 等分协议的 connectionStateChange 回调，同一耳机常同时挂多个协议。
- [封装 startBLEScan 等声明为 void 的同步系统接口时查 @throws，在服务层 try/catch 收敛为失败状态，页面检查结果并复位进行中状态](lesson-7ed00c55221c0f935d95.lesson.md)
  - 时机：服务层与页面实现阶段，封装 BLE 扫描等可能同步抛 BusinessError 的系统接口，并决定页面的失败态时
  - 情境：目标端用 @ohos.bluetooth.ble 的 startBLEScan/stopBLEScan 等在 d.ts 中声明为 void 的同步接口；源端用 BluetoothState、蓝牙关闭恢复卡、扫描启动异常类等显式建模适配器关闭与扫描失败；决策要求失败降级、不崩溃。
- [源端在应用内直接开关蓝牙时，先查 @ohos.bluetooth.access 的开关接口与权限再定方案，不把现有的设置跳转当作平台限制](lesson-7a081dc36013a60358ac.lesson.md)
  - 时机：规格提取、增量规格与服务实现阶段，为源端在应用内直接开关的蓝牙确定目标实现与验收项时；以及真机安装因权限被拒而调整权限清单时
  - 情境：源端点击开关后在应用内调用 BluetoothAdapter.enable()/disable()；决策只允许“平台不允许应用直接完成的开关”改走系统授权弹窗或设置跳转；现有目标代码已把 enable/disable 写成打开系统蓝牙设置，或权限清单里有从第三方文档抄来的系统级权限。
  - 例外：目标最低 API 与设备上确无可用的应用内开关接口，且决策已批准设置跳转
- [蓝牙开关以终态回读为准：状态回调后读 getState，过渡态与迟到回调不写成关闭；门控放在决策点实时读取](lesson-29922f57cc365ff3d638.lesson.md)
  - 时机：系统能力接入与状态接线阶段，决定蓝牙开关/可用状态以什么为真值、在何处门控、初始加载按什么顺序赋值时
  - 情境：源端在点击与广播处理时实时读 BluetoothAdapter，只在 ACTION_STATE_CHANGED 的 STATE_ON/STATE_OFF 终态刷新 UI；目标用 access.on('stateChange') 与 access.getState()，经 ViewModel 与页面 @Local 副本驱动开关、设备入口和二级连接页。

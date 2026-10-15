# app/bluetooth

蓝牙能力：适配器开关状态的真值、门控与初始加载，分协议连接状态的聚合与成功判定，应用内开关蓝牙的方式，扫描等同步接口的抛错收敛与失败态

[上一级](../index.md)

## 本级经验

- [封装声明为 void 的同步系统接口（如 startBLEScan）时读 d.ts 的 @throws，在服务层 try/catch 收敛为失败状态](lesson-7ed00c55221c0f935d95.lesson.md)
  - 时机：服务层与页面实现阶段，封装 BLE 扫描等可能同步抛 BusinessError 的系统接口，并决定页面的失败态时
  - 情境：目标调用的系统接口在 d.ts 中返回 void 且列有 @throws BusinessError 错误码（如 @ohos.bluetooth.ble 的 startBLEScan/stopBLEScan）；源端对适配器关闭、扫描启动失败有显式状态或异常类型，或决策要求失败降级、不崩溃。
- [源端在应用内直接开关蓝牙时，先查 @ohos.bluetooth.access 的开关接口与权限再定方案，不把现有的设置跳转当作平台限制](lesson-7a081dc36013a60358ac.lesson.md)
  - 时机：规格提取、增量规格与服务实现阶段，为源端在应用内直接开关的蓝牙确定目标实现与验收项时；以及真机安装因权限被拒而调整权限清单时
  - 情境：源端点击开关后在应用内调用 BluetoothAdapter.enable()/disable()；决策只允许“平台不允许应用直接完成的开关”改走系统授权弹窗或设置跳转；现有目标代码已把 enable/disable 写成打开系统蓝牙设置，或权限清单里有从第三方文档抄来的系统级权限。
  - 例外：目标最低 API 与设备上确无可用的应用内开关接口，且决策已批准设置跳转
- [源端在点击瞬间实时读取蓝牙等系统开关做门控时，目标在 ViewModel 决策点实时回读，初始加载先同步取系统状态](lesson-4c3a4c6cf51b0787ee85.lesson.md)
  - 时机：页面与 ViewModel 接线阶段，决定蓝牙等系统开关状态在何处门控导航、初始加载按什么顺序给开关赋值时
  - 情境：源端点击入口时实时调用 BluetoothAdapter.isEnabled() 一类接口决定是否进入下一页，初始化时先同步读系统开关再读偏好；目标准备用页面 @Local 副本做入口拦截，或把系统状态放在权限、偏好、通知授权等多个 await 之后一次性赋值。
- [目标用 A2DP、HFP 等分协议回调判断耳机连接时按设备聚合：所监听协议都断开才判定设备断开，成功提示以回调或回读确认](lesson-ecc67592eba3402c0a1f.lesson.md)
  - 时机：实现蓝牙设备连接、断开状态与“连接/断开成功”判定时
  - 情境：源端用 ACTION_ACL_CONNECTED/ACTION_ACL_DISCONNECTED 等设备级广播判断连接与断开；目标改用 A2DP、HFP 等分协议的 connectionStateChange 回调，同一耳机常同时挂多个协议。
  - 例外：源端本身只监听某一 profile 的 ACTION_CONNECTION_STATE_CHANGED（如只关心 A2DP 播放）时，按该协议判定，不做设备聚合
- [订阅蓝牙 access.on('stateChange') 驱动开关时以 getState 终态回读为准，过渡态与迟到回调不写成关闭](lesson-29922f57cc365ff3d638.lesson.md)
  - 时机：系统能力接入与状态接线阶段，决定蓝牙开关/可用状态以回调参数还是系统回读为真值时；重写已有蓝牙状态处理时
  - 情境：源端只在 ACTION_STATE_CHANGED 的 STATE_ON/STATE_OFF 终态刷新 UI，或在变化时回读 BluetoothAdapter.isEnabled()；目标用 access.on('stateChange') 与 access.getState()，准备把回调参数直接写成开关值。
  - 例外：源端本身按 EXTRA_STATE 的全部取值（含 TURNING_*）驱动界面时，按源端分支逐一映射

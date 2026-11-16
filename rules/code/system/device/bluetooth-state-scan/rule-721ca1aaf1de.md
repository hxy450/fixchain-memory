# 封装声明为 void 却带 @throws 的同步系统接口时，服务层 try/catch 收敛成返回值

审的是：代码
触发（任一种）：
- 读到：鸿蒙 SDK 声明里 `startBLEScan(...)`、`stopBLEScan()` 返回 `void`，注释列有 `@throws { BusinessError } 2900003 - Bluetooth disabled.` 等错误码；写错的样子：服务层直接调用 `ble.startBLEScan(...)` / `ble.stopBLEScan()`，外面没有 `try/catch`，调用后直接置 `scanning = true`
适用范围：服务层封装可能同步抛 BusinessError 的系统接口（如 BLE 扫描）时
做法：
- 封装前除签名外同时查该接口 d.ts 的 @throws 错误码段
- 写成 `try { ble.startBLEScan(filters, options); return true; } catch (e) { this.lastScanError = (e as BusinessError).code; return false; }`，stopBLEScan 同样包住；不让 BusinessError 冒泡到点击回调
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- function startBLEScan(filters: Array<ScanFilter>, options?: ScanOptions): void；@throws 201、401、801、2900001 Service stopped、2900003 Bluetooth disabled、2900099 Operation failed：返回 void，失败靠同步抛 BusinessError（出处：鸿蒙 SDK 的 ets/api/@ohos.bluetooth.ble.d.ts，ble.startBLEScan）
- function stopBLEScan(): void；@throws 201、801、2900001、2900003、2900099：停止扫描同样会同步抛错（出处：鸿蒙 SDK 的 ets/api/@ohos.bluetooth.ble.d.ts，ble.stopBLEScan）
- BusinessError<T = void> extends Error，code: number：catch 到的错误按 code 区分原因（出处：鸿蒙 SDK 的 ets/api/@ohos.base.d.ts，BusinessError）
- 蓝牙关闭时 startBLEScan 抛 2900003 未捕获，进程被杀（PROCESS_KILL / Js Error）；包 try/catch 后不再崩溃：不捕获的后果（出处：卡里修好并验证过）
- connect(): void，@throws 2900003 等：同族接口：GattClientDevice 的连接，同样同步抛错（出处：鸿蒙 SDK 的 ets/api/@ohos.bluetooth.ble.d.ts，GattClientDevice.connect）
- disconnect(): void，@throws 2900003 等：同族接口：GattClientDevice 的断开（出处：鸿蒙 SDK 的 ets/api/@ohos.bluetooth.ble.d.ts，GattClientDevice.disconnect）
未核实：卡里记的鸿蒙 SDK 是 6.1.1(24)，本机核实用 API 23；2900003 出自修复期设备日志
来源：1 张卡，1 个应用
- case-424ce07c14ab153d3920（Meshtastic）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断；取值 4 ← 诊断

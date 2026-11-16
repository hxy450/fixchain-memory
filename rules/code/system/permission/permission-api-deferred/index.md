# 调用声明带 @permission 的接口时的权限声明和移交登记

agent 会看到什么：交回的代码调用 sensor.on(SensorId.ACCELEROMETER / GYROSCOPE)、MediaAssetChangeRequest.deleteAssets 这类声明带 @permission 的接口，本切片不管 module.json5；产物里 requestPermissions 没有对应权限，交回里也没登记 deferred-work / 移交项

## 规矩

- rule-08298c6ba10b｜调用带 @permission 的接口而本切片不管 module.json5 时，登记 deferred-work｜写错：代码调用 sensor.on(sensor.SensorId.ACCELEROMETER / GYROSCOPE, …) 或 MediaAssetChangeRequest.deleteAssets，module.json5 requestPermissions 里没有对应权限，本切片的交回里也没登记 deferred-work / 移交项

# 权限

源端申请定位、媒体、存储等运行时权限并有拒绝分支，目标端有 requestPermissionsFromUser、checkAccessTokenSync 和 module.json5 的权限声明时

## 触发族

- [定位权限（ACCESS_FINE / COARSE_LOCATION）的申请和判定](location-permission/index.md)（4 条）：读过的源码里申请 ACCESS_FINE_LOCATION 和 ACCESS_COARSE_LOCATION（PermissionX、requestPermissions）、调 isLocationEnabled、入口先判定位权限；交回的 requestPermissionsFromUser / checkAccessTokenSync 只列一项、要求全部授予、先查位置开关后授权，或入口没设门槛
- [权限拒绝、服务关闭或无坐标时的失败分支](permission-denied-branch/index.md)（3 条）：读过的源码里权限拒绝、定位服务关闭、无坐标时仍有反馈、错误提示或按城市的另一条查询；交回的仓库方法开头 return [] 短路，或 UI 只写了成功分支、errorMessage 没展示
- [媒体与存储类权限的权限名和声明](media-storage-permission/index.md)（2 条）：读过的源码里申请 READ_MEDIA_AUDIO、READ_EXTERNAL_STORAGE 或 Dart 的 Permission.storage；交回的 requestPermissionsFromUser 申请的权限名和后续调用的接口对不上、module.json5 没声明，或 OHOS 上仍被安卓专用的权限门控拦住
- [调用声明带 @permission 的接口时的权限声明和移交登记](permission-api-deferred/index.md)（1 条）：交回的代码调用 sensor.on(SensorId.ACCELEROMETER / GYROSCOPE)、MediaAssetChangeRequest.deleteAssets 这类声明带 @permission 的接口，本切片不管 module.json5；产物里 requestPermissions 没有对应权限，交回里也没登记 deferred-work / 移交项

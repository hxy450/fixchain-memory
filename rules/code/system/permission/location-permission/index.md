# 定位权限（ACCESS_FINE / COARSE_LOCATION）的申请和判定

agent 会看到什么：读过的源码里申请 ACCESS_FINE_LOCATION 和 ACCESS_COARSE_LOCATION（PermissionX、requestPermissions）、调 isLocationEnabled、入口先判定位权限；交回的 requestPermissionsFromUser / checkAccessTokenSync 只列一项、要求全部授予、先查位置开关后授权，或入口没设门槛

## 规矩

- rule-925c964071f5｜源端请求 FINE+COARSE 定位时，授权列表同时含模糊和精确两项定位权限｜读到：源端同时请求 Manifest.permission.ACCESS_FINE_LOCATION 和 ACCESS_COARSE_LOCATION（如 PermissionX.permissions(...)、requestPermissions(...)）；写错：授权检查和申请只 checkAccessTokenSync / requestPermissionsFromUser 'ohos.permission.LOCATION' 一项
- rule-74191eab0015｜定位权限把 APPROXIMATELY_LOCATION 与 LOCATION 当一组判定，任一授予就继续｜读到：源端同时声明 ACCESS_COARSE_LOCATION 与 ACCESS_FINE_LOCATION，两者都处理；写错：requestPermissionsFromUser(context, [APPROXIMATELY_LOCATION, LOCATION]) 之后用 for 循环遍历 authResults，任一项 !== 0 就 return false（照搬通用「全部授予」模板），只授予模糊位置时定位被判为拒绝
- rule-4f6f03374205｜规格写先授权再定位时，链路写成授权 → isLocationEnabled → 定位｜读到：源端先 isLocationEnabled() 检查 GPS 开关再请求权限；规格数据流写「确保授权 → 系统位置能力可用性检查 → 定位」，验收要求授权前不启动定位；写错：目标沿用源端顺序，先 geoLocationManager.isLocationEnabled() 再 requestPermissionsFromUser
- rule-7e32e84a677c｜源端入口无定位权限时转别的页，目标入口照样设门槛，不让无坐标状态以空列表进附近页｜读到：源端入口的 setOnClickListener 里先判定位权限，无权限时转去选城页面，不进附近列表；写错：目标入口的 onClick 里直接跳附近页，没有判定位权限或坐标是否可用

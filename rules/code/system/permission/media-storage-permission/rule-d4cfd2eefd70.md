# requestPermissionsFromUser 的权限要对上接口声明并在 module.json5 声明

审的是：代码
触发（任一种）：
- 读到：规格或验收条目写「音频库读取权限 + requestPermissionsFromUser，拒绝→引导空态」，安卓端是 READ_MEDIA_AUDIO / READ_EXTERNAL_STORAGE；写错的样子：requestPermissionsFromUser 申请 ohos.permission.READ_AUDIO，授权后调用的却是 photoAccessHelper 的 getAssets（声明要 READ_IMAGEVIDEO）或 AudioViewPicker（不用权限）
- 读到：module.json5 的 requestPermissions 里对应权限那段被注释或删掉；写错的样子：代码里 requestPermissionsFromUser 仍申请这项权限，点击后不弹窗、没反应
适用范围：鸿蒙代码里写运行时权限门（requestPermissionsFromUser 后再调受保护接口）的地方
做法：
- requestPermissionsFromUser(context, [...]) 里的每项权限，照授权后要调用的接口在声明里的 @permission 写；走 picker（如 AudioViewPicker）的路径不申请权限，删掉权限查询和申请链，按钮直接拉起 picker
- module.json5 的 requestPermissions 有改动时，把所有 requestPermissionsFromUser 调用点对一遍：申请的每项都要有激活的声明
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- requestPermissionsFromUser(context: Context, permissionList: Array<Permissions>): Promise<PermissionRequestResult>：动态申请权限（出处：鸿蒙 SDK 的 ets/api/@ohos.abilityAccessCtrl.d.ts，AtManager.requestPermissionsFromUser）
- authResults 里 0 是已授权、-1 是未授权、2 是请求无效：申请没声明的权限时拿到 2，不会弹窗（出处：鸿蒙 SDK 的 ets/api/security/PermissionRequestResult.d.ts，PermissionRequestResult.authResults）
- errorReasons 里 2 表示申请的权限没有声明（@since 18）：用来判断是不是 module.json5 漏了声明（出处：鸿蒙 SDK 的 ets/api/security/PermissionRequestResult.d.ts，PermissionRequestResult.errorReasons）
- PhotoAccessHelper.getAssets 的 @permission 是 ohos.permission.READ_IMAGEVIDEO：申请 READ_AUDIO 对它没用（出处：鸿蒙 SDK 的 ets/api/@ohos.file.photoAccessHelper.d.ts，PhotoAccessHelper.getAssets）
- Picker 接口本身无需申请权限：走 AudioViewPicker 时不写权限门（出处：select-user-file.md，选择用户文件）
- 申请 user_grant 权限的第一步是在配置文件中声明应用需要请求的权限：module.json5 的 requestPermissions 里要有这项（出处：request-user-authorization.md，向用户申请授权）
未核实：卡里的行为在 target SDK 6.1.1(24) 下观察，本机核实用的声明是 API 23
来源：1 张卡，1 个应用
- case-1607d055621c41c4c087（免费来电多多）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4

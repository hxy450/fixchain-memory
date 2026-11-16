# 源端拉起相机前有能力预检和权限申请时，目标逐段写出，不用 pick 的 catch 代替

审的是：代码
触发（任一种）：
- 读到：拍照方法里先做相机能力预检（hasSystemFeature 或 isAvailable(…FEATURE_CAMERA) 为假就提示并 return），再运行时申请 CAMERA 权限，回调里才建文件、拉相机；写错的样子：直接 await cameraPicker.pick(...)，catch 注释成「预检失败分支等价」；没有能力预检，也没有 ohos.permission.CAMERA 申请
适用范围：源端拉起相机、外部意图等系统能力前带门控（能力预检、运行时权限）的服务层实现
做法：
- 对照源方法逐段写「预检 → 权限 → 拉起 → 结果」，缺一段即为偏差；预检写成 canIUse('SystemCapability.Multimedia.Camera.Core') 或能力查询，为 false 时走源端的提示并 return
- 权限写成 abilityAccessCtrl.createAtManager().requestPermissionsFromUser(context, ['ohos.permission.CAMERA'])，并在 module.json5 声明；拒绝时不建文件、不拉起，通过后才 cameraPicker.pick(...)
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- canIUse(syscap: string): boolean：按系统能力名判断当前设备是否支持（出处：鸿蒙 SDK 的 ets/api/@internal/full/global.d.ts，canIUse）
- pick(context: Context, mediaTypes: Array<PickerMediaType>, pickerProfile: PickerProfile): Promise<PickerResult>；@syscap SystemCapability.Multimedia.Camera.Core：拉起系统相机，所属系统能力名就是预检要查的那个（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.cameraPicker.d.ts，cameraPicker.pick）
- createAtManager(): AtManager；requestPermissionsFromUser(context: Context, permissionList: Array<Permissions>): Promise<PermissionRequestResult>：运行时向用户申请权限（出处：鸿蒙 SDK 的 ets/api/@ohos.abilityAccessCtrl.d.ts，abilityAccessCtrl.createAtManager、AtManager.requestPermissionsFromUser）
- 补上相机能力预检和 ohos.permission.CAMERA 申请后，拒绝时不建附件、不发起拍摄，与源端一致：修好后的写法（出处：卡里修好并验证过）
未核实：卡里的行为出自 API 24（HarmonyOS 6.1.1），本机按 API 23 核对声明；官方文档说 CameraPicker 无需申请相机权限；这里的权限申请是为复刻源端「拒绝即不拍」的门控
来源：1 张卡，1 个应用
- case-29db923e9cadbe8ce53c（omni-notes-hmos）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1、诊断；取值 4 ← 诊断

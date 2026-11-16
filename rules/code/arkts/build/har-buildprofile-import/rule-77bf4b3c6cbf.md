# 带构建开关的服务下沉到 HAR 后，宿主每个入口调用初始化时都传宿主的 DEBUG

审的是：代码
触发（任一种）：
- 读到：下沉前的服务自己 import { DEBUG } from 'BuildProfile' 决定行为，宿主的 UIAbility、FormExtensionAbility、WorkSchedulerExtensionAbility、BackupExtensionAbility 里都调用它的 initialize()；写错的样子：宿主入口只把导入改成从 HAR 模块名导入，仍调用无参的 initialize()，没有传 DEBUG；或只改了主 UIAbility，漏了卡片、WorkScheduler、备份扩展
适用范围：把原先自己读 BuildProfile 的服务下沉到 HAR、开关改成初始化参数之后，宿主侧的所有调用入口
做法：
- 在宿主每个调用入口 import { DEBUG } from 'BuildProfile'，调用写成 initialize(DEBUG)
- 入口逐个对：UIAbility.onCreate、FormExtensionAbility.onAddForm、WorkSchedulerExtensionAbility.onWorkStart、BackupExtensionAbility.onBackup / onRestore 里凡调用初始化的都改
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): void：主 UIAbility 的入口回调（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.UIAbility.d.ts，UIAbility.onCreate）
- onAddForm(want: Want): formBindingData.FormBindingData：卡片扩展的入口回调（出处：鸿蒙 SDK 的 ets/api/@ohos.app.form.FormExtensionAbility.d.ts，FormExtensionAbility.onAddForm）
- onWorkStart(work: workScheduler.WorkInfo): void：延迟任务扩展的入口回调（出处：鸿蒙 SDK 的 ets/api/@ohos.WorkSchedulerExtensionAbility.d.ts，WorkSchedulerExtensionAbility.onWorkStart）
- onBackup(): void；onRestore(bundleVersion: BundleVersion): void：备份恢复扩展的两个入口回调（出处：鸿蒙 SDK 的 ets/api/@ohos.application.BackupExtensionAbility.d.ts，BackupExtensionAbility.onBackup、BackupExtensionAbility.onRestore）
针对本应用要查的：
- 宿主里有哪些入口调用了这个服务的初始化：宿主 HAP 的 module.json5 里 abilities 和 extensionAbilities 列出的各个入口类文件；逐个入口搜初始化调用，凡是无参调用的都改成传 DEBUG
来源：1 张卡，1 个应用
- case-282d676ed02777809cac（记得日历）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2、诊断

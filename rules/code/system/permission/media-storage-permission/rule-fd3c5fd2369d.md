# Dart 里 Android 专用权限门控只保护写应用私有目录时，为 OHOS 加最小跳过分支

审的是：代码
触发（任一种）：
- 读到：Dart 代码无条件 await Permission.storage.request()（或 manageExternalStorage），被门控的操作只写 getApplicationDocumentsDirectory() 一类应用私有目录；写错的样子：目标保持该文件冻结、没有 Platform.isOhos 分支，OHOS 上权限被拒后直接返回 null，下载或保存失败
适用范围：Flutter 应用迁 OHOS、dart-adapted 阶段扫描 Dart 里 Android 专用权限门控时
做法：
- 除 Platform 分支外，也扫描无条件的 Android 专用权限门控（Permission.storage、manageExternalStorage 等）
- 被门控的操作只写应用私有目录时，在权限检查开头加 if (Platform.isOhos) return true;，其他平台仍照原样请求权限
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 应用可以在「应用文件目录」下保存和处理自己的应用文件：OHOS 上写应用私有目录不需要存储权限（出处：app-sandbox-directory.md，概述）
- Context#getDataDir 下的文件读写不需要额外权限：源端写私有目录本来也不靠存储权限，跳过门控不改变语义（出处：android.content.Context#getDataDir）
未核实：Platform.isOhos 出自 Flutter 的 OHOS 版 dart:io，三类来源里没核实
来源：1 张卡，1 个应用
- case-3cc99a6c512ab85ed874（app-photo-shop-flutter）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2、诊断

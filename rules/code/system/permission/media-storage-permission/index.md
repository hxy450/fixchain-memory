# 媒体与存储类权限的权限名和声明

agent 会看到什么：读过的源码里申请 READ_MEDIA_AUDIO、READ_EXTERNAL_STORAGE 或 Dart 的 Permission.storage；交回的 requestPermissionsFromUser 申请的权限名和后续调用的接口对不上、module.json5 没声明，或 OHOS 上仍被安卓专用的权限门控拦住

## 规矩

- rule-d4cfd2eefd70｜requestPermissionsFromUser 的权限要对上接口声明并在 module.json5 声明｜读到：规格或验收条目写「音频库读取权限 + requestPermissionsFromUser，拒绝→引导空态」，安卓端是 READ_MEDIA_AUDIO / READ_EXTERNAL_STORAGE；写错：requestPermissionsFromUser 申请 ohos.permission.READ_AUDIO，授权后调用的却是 photoAccessHelper 的 getAssets（声明要 READ_IMAGEVIDEO）或 AudioViewPicker（不用权限）
- rule-fd3c5fd2369d｜Dart 里 Android 专用权限门控只保护写应用私有目录时，为 OHOS 加最小跳过分支｜读到：Dart 代码无条件 await Permission.storage.request()（或 manageExternalStorage），被门控的操作只写 getApplicationDocumentsDirectory() 一类应用私有目录；写错：目标保持该文件冻结、没有 Platform.isOhos 分支，OHOS 上权限被拒后直接返回 null，下载或保存失败

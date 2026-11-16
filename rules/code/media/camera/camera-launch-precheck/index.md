# 拉起相机前的能力预检和权限申请

agent 会看到什么：读到拍照方法里先 hasSystemFeature / isAvailable(…FEATURE_CAMERA) 预检、再运行时申请 Manifest.permission.CAMERA，回调里才建文件、拉相机；产物里直接 await cameraPicker.pick(...)，用 catch 顶替预检和 ohos.permission.CAMERA 申请

## 规矩

- rule-02a7023dbfd7｜源端拉起相机前有能力预检和权限申请时，目标逐段写出，不用 pick 的 catch 代替｜读到：拍照方法里先做相机能力预检（hasSystemFeature 或 isAvailable(…FEATURE_CAMERA) 为假就提示并 return），再运行时申请 CAMERA 权限，回调里才建文件、拉相机；写错：直接 await cameraPicker.pick(...)，catch 注释成「预检失败分支等价」；没有能力预检，也没有 ohos.permission.CAMERA 申请

# 预签名上传的诊断日志包

agent 会看到什么：读过的源码里上传函数先取 presign 地址再 PUT，打包日志目录、设备信息和 ObjectBox 分表 TXT，清单有 android:usesCleartextTraffic；交回的代码里网络层对上传地址的 https 校验和归档里装了什么

## 规矩

- rule-ca7ff3fd7427｜诊断归档照安卓上传函数逐项对齐日志目录、设备信息和各表 TXT，不用快照或整库代替｜读到：安卓上传函数先写设备信息 TXT，把 ObjectBox 的各个 Box 逐表导出成 TXT，flush 后把日志目录递归压进 ZIP；写错：目标归档只放 BqLog 的 `take_snapshot()` 当日快照或一个诊断 JSON，或者用整库数据库文件代替分表 TXT，没有收集日志目录里的全部留存文件
- rule-0dec6bf55cba｜预签名上传地址可能是 http 时，网络层按端点放行明文，其余请求仍只接受 https｜读到：安卓清单写了 android:usesCleartextTraffic="true"，上传地址由 presign 接口返回后原样 PUT；写错：目标网络层对 Raw 端点的绝对 URL 一律做 `https://` 前缀校验、不是就抛错，或者把返回的 http 地址自动改写成 https

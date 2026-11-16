# MediaRecorder 迁成 AVRecorder 的录制控制

agent 会看到什么：读到源端 MediaRecorder 的 prepare / start / stop（stop 后立即置 null、抛 RuntimeException 时删坏片）、依赖同步时序的重复录制计数，或带当次录制档位对象的错误上报；产物里 AVRecorder 的 Promise 链、停录的并发守卫和取消检查、失败分支的标志复位和回传，以及上报传的是不是档位对象

## 规矩

- rule-5a89775af0c4｜AVRecorder 停录发起即登记并返回共享 Promise，prepare/start 链每步 await 后查取消｜读到：源端 MediaRecorder.stop() 同步完成后立即把录制器置为 null，以 null 守卫挡住重复停止；写错：停录方法每次都独立调 recorder.stop()，只在 stop() 兑现后才置空；prepare(...).then(...start()) 的回调链不检查是否已被要求停止，准备期间的停止因尚未开始直接返回
- rule-f95419a47eec｜AVRecorder.stop 失败时在 finally 复位录制中标志，删坏片并回传空 URI｜读到：源端 MediaRecorder.stop() 抛 RuntimeException 时删掉输出文件（坏片）；写错：stop 失败分支删了坏片仍以原 URI 回调停录结果；录制中标志只在 release() 里复位，recorder.stop() 失败后仍为 true
- rule-ff0dd5cd5a00｜依赖同步时序的重复计数迁到异步启动时，在发起端同步初始化，用参数区分首段和重复段｜读到：源端重复次数在 takePicture() 同步返回后才递减（注释说明避免被重置），启动回调里「剩余为 0 才初始化」在同步调用中执行；写错：初始化放进 prepare().then(() => start().then(...)) 之后的回调，递减却在启动函数同步返回后立即执行
- rule-12c36476e0c9｜错误特征或错误上报方法带对象参数时，目标保留对象参数，不用 boolean 或空对象占位｜读到：源端错误特征方法接收对象参数（如当次录制档位），按它的多个字段和偏好判定后用 R.string 标签以「/」拼接；停录出错时以 getter 取当次对象上报；写错：目标把参数简化成 boolean 并推字面量，或上报时用 `null as object`、无参 new 出的空对象占位；下游控制器不保存、不传递当次对象

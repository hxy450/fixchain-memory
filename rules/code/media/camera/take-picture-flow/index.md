# 拍照调用和它的回调（takePicture、PhotoOutput.capture）

agent 会看到什么：读到源端 takePicture(pictureCallback, errorCallback)、拍照函数里构造的回调对象、拍照前 setRotation / JPEG_ORIENTATION、长按连拍和多帧结果回调；产物里桥接契约的 takePicture 签名、编排器的完成 / 失败入口和请求代数、PhotoCaptureSetting.rotation、photoAssetAvailable 的结果分派和连拍循环

## 规矩

- rule-fcfd74917aee｜源端拍照带完成和失败回调时，桥接契约要回传完成 / 失败，编排器在入口里复位状态和续拍｜读到：源端以 takePicture(pictureCallback, errorCallback) 发起拍照：完成回调里复位拍照状态、续拍剩余的重复张数、按偏好暂停预览，失败回调重启预览；写错：桥接接口把拍照定义成无参无回调的 takePicture: () => void；编排器没有完成 / 失败入口，拍照中的状态没有复位点，续拍函数没有调用者，暂停预览没实现
- rule-47960b4fd94f｜移植构造回调对象的拍照函数时，逐个给回调列出目标端落点，桥接契约带上它们要的查询和事件｜读到：源函数本体里构造回调对象（含多个 on… 回调，如补光开启、完成），在函数尾交给 takePicture(…) 之类的拍照调用；写错：目标函数只剩阶段置位和一句 takePicture() 调用，源回调对象里的分支在目标端没有落点；桥接接口里没有这些回调要用的查询或事件成员
- rule-edc44088df54｜新增取消补光等待的路径时，复用已有的请求代数作废机制，使迟到的对焦回调不再拍照｜写错：新加的取消函数只复位阶段标志等状态，没有让编排器已有的请求代数加一，而已登记的对焦续拍回调按这个代数判断是否继续调 takePicture()
- rule-1f5bcd228a41｜拍照前 setRotation 的 JPEG 角度，目标用 getPhotoRotation 填 rotation｜读到：源端拍照函数本体里先 `setRotation(getImageVideoRotation())` 或给 `CaptureRequest.JPEG_ORIENTATION` 设值，再拍照；写错：目标端 `photoOutput.capture(...)` 的 `PhotoCaptureSetting` 里没有 `rotation`，拍照前不下发旋转
- rule-623347ea3bb2｜photoAssetAvailable 没有拍摄 ID，超时或失败时退役 PhotoOutput 并重建会话｜读到：`photoAssetAvailable` 回调只交付 `PhotoAsset`，不带 capture 或请求 ID；写错：回调把资产交给当时唯一的结果接收者；拍照超时只清空接收者，同一 `PhotoOutput` 继续订阅，上一张迟到的资产被下一次拍摄收到
- rule-f3a41fd4417d｜规格要求布尔参数开启连拍时，编排层自建连拍循环，不用 void 吞掉参数｜读到：规格的 AC 写明某个布尔参数为 true 时要「长按后连续多帧 onPictureTaken」，源端长按快门持续出帧、松手停止；写错：拍照编排函数里用 `void 参数名;` 丢弃这个标志，只走一次单拍；编排器里没有连拍循环、在途帧状态和停止连拍的方法
- rule-57b0f9aafb44｜接线时发现桥接只有单帧且无完成回调，登记 FWD-REF 回编排器补契约，不在保存侧单图入队｜读到：源端或目标端的应用接口已声明接收 ArrayBuffer[] 的整组结果回调，和「所有图片回调返回后调用」的完成回调；写错：接线时保存侧把多帧模式按单图入队（images = [data]，注释写多帧后缀却只给一张）、失败只弹 toast，没有登记 FWD-REF

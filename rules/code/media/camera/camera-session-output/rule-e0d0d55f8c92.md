# photoAvailable 的 byteBuffer 要异步消费时，先 slice(0) 复制再释放 Photo

审的是：代码
触发（任一种）：
- 读到：源端 onImageAvailable 里先把 JPEG 复制成 byte[] 再 image.close()；目标的保存服务把字节排进后台队列异步保存；写错的样子：photoAvailable 回调里 getComponent 之后立即 photo.release()，再把同一个 component.byteBuffer 交给异步保存，中间没有复制
适用范围：拍照回调取出的 JPEG 字节在回调返回后才被消费时
做法：
- await photo.main.getComponent(image.ComponentType.JPEG) 后先 const bytes = component.byteBuffer.slice(0) 复制，再在 finally 里 photo.release()，把复制出的 bytes 交给保存队列
- 不复制时，把 release 放到字节消费完成后的 finally 里；不能先释放再用同一个 ArrayBuffer
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- interface Photo { main: image.Image; release(): Promise<void> }：Photo 持有主图，release 释放 Photo 对象（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，camera.Photo）
- getComponent(componentType: ComponentType): Promise<Component>：从 image.Image 取指定分量（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.image.d.ts，Image.getComponent）
- readonly byteBuffer: ArrayBuffer：Component 的分量数据，是 Photo 所持原生图像的缓冲（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.image.d.ts，Component.byteBuffer）
- close() 之后再读写先前 getBuffer 得到的 ByteBuffer 行为未定义：源端先复制再 close 的原因（出处：android.media.Image#close）
- await getComponent → byteBuffer.slice(0) → finally 中 release：返修后的写法（出处：卡里修好并验证过）
未核实：SDK 声明没写 byteBuffer 在 Photo.release 之后的有效期；卡里环境是 API 24（HarmonyOS 6.1.1），本机声明是 API 23
来源：1 张卡，1 个应用
- case-b49b06a3f59e5828d836（opencamera-hmos）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 5 ← 诊断

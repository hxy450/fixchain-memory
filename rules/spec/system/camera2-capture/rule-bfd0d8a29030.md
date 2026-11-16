# 抽取原生图像回调时，规格把「先复制字节再 close」写成验收条目

审的是：规格
触发（任一种）：
- 读到：源端 onImageAvailable 里先把 JPEG 复制到 byte[] 再 image.close()；写错的样子：规格只抽出「无回调时立即 close」，没有「先复制字节再 close / release」的验收条目
适用范围：规格里抽取 onImageAvailable 这类原生图像回调的验收条目
做法：
- 验收写明：回调交出的字节若被异步消费，先复制再释放（目标端 component.byteBuffer.slice(0) 之后再 photo.release()）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- close() 之后再读写先前 getBuffer 得到的 ByteBuffer 行为未定义：源端先复制再 close 的原因（出处：android.media.Image#close）
来源：1 张卡，1 个应用
- case-b49b06a3f59e5828d836（opencamera-hmos）：做法第 1 步 ← 建议 4、诊断

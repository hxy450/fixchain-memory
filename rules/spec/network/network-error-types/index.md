# 按异常类型分类的网络失败

agent 会看到什么：源端 catch 链按 SocketTimeoutException / UnknownHostException / IOException 等异常类型和 e.getMessage() 分支；规格错误码表里的判据

## 规矩

- rule-b9a0e20b5f87｜源端按异常类型分类网络失败时，规格的错误码表写出 BusinessError.code 判据｜读到：源端 catch 链按 IllegalArgumentException / SocketTimeoutException / UnknownHostException / IOException（含证书消息）分支，详情用 e.getMessage()；写错：规格的错误码表只以 Java 异常类名和 Java 消息字面量（如 'Trust anchor for certification path not found'）为判据；实现映射表里没有「Java 异常类型 → BusinessError.code」一行

# MIFARE Classic 标签接口

agent 会看到什么：读过的源码里用 android.nfc.Tag、MifareClassic 的 authenticateSectorWithKeyA/B（返回 boolean）；交回的代码里当前标签存成 TagInfo 还是 MifareClassicTag、authenticateSector 的 reject 和错误码怎么分流

## 规矩

- rule-f2ae883ff85e｜源全局当前标签是 android.nfc.Tag 时，目标存 TagInfo，不收窄成 MifareClassicTag｜读到：全局当前标签字段类型是 android.nfc.Tag，setTag 对任何技术的卡都赋值，之后才判断是否支持 MIFARE Classic；写错：目标全局状态把当前标签声明成 tag.MifareClassicTag，非 MIFARE Classic 卡写入 null，在场判断写成 `!== null`
- rule-dad65408043e｜源 API 以 false 表示被拒、目标只会 reject 时，先写单次适配器区分被拒与丢卡，重试都经它｜读到：源码 ret = authenticateSectorWithKeyA/B(...) 取 boolean，ret 为 false 时按偏好重试，只有 IOException、TagLostException 这类异常才立即返回 false；写错：目标的认证方法 try { await ….authenticateSector(...) } catch { return false }：任何 reject 都直接返回，「被拒后重试」的分支永远走不到
- rule-e82cfe35da8a｜靠 d.ts 没说明语义的错误码分流被拒与丢卡时，加 isConnected() 在场复核并登记真机待验｜读到：目标 d.ts 里 authenticateSector 只列 BusinessError 201/401/3100201/3100204，没说哪个码是密钥被拒、哪个是丢卡；写错：适配器只按单个 err.code（3100201 或 3100204）判被拒或丢卡，没有 isConnected() 这类在场复核，码值假设也没进真机待验项

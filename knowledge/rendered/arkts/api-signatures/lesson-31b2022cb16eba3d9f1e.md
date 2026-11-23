# MessageDigest 改用 cryptoFramework Md 时，空输入不调用 update，直接返回该算法的空输入摘要

## 何时使用

实现阶段，把对可能为空的字符串求摘要（缓存键、内容哈希）的 MessageDigest 调用改写为 cryptoFramework.createMd 时

## 适用情境

源端对可能为空的字段（标题、摘要文本等）无条件求摘要，空串是正常路径；目标用 cryptoFramework.createMd + update({ data }) + digest()。

## 例外与边界

- 第 1 步给的常量是 SHA-256 的小写十六进制形式；源端用的是别的算法（如 MD5、SHA-1），或把摘要编码成大写十六进制、Base64 等其他形式时，空输入要返回同一算法、同一编码下的值，和非空路径的输出格式一致，否则同一内容得到的键与源端不同。

## 原因

已观察到 Md.update 传入零长度 DataBlob 时运行期抛错（build context fail.），而源端对空串照常返回摘要；空字段在目标中断整个调用。文档写明 Md 的 digest 必选、update 可选，只调用 digest() 不调用 update 符合接口约定，卡里尚未在干净构建上验证。

## 做法

1. 输入为空时不调用 update，直接返回该算法对空输入的标准摘要（SHA-256("") = e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855）；非空才 update 后 digest。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕cryptoFramework 的 Md.update 传入零长度 DataBlob 时运行期抛错，错误信息为 build context fail.
- 〔原因 / 做法第 1 步〕Md 的 update 和 digest 是两段式接口，需要成组使用，其中 digest 必选、update 可选

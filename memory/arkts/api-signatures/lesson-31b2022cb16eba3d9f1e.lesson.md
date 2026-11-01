# MessageDigest 改用 cryptoFramework Md 时，空输入不调用 update，直接返回该算法的空输入摘要

ID：`lesson-31b2022cb16eba3d9f1e` · 版本：2

[本主题](index.md)

## 何时使用

实现阶段，把对可能为空的字符串求摘要（缓存键、内容哈希）的 MessageDigest 调用改写为 cryptoFramework.createMd 时

## 适用情境

源端对可能为空的字段（标题、摘要文本等）无条件求摘要，空串是正常路径；目标用 cryptoFramework.createMd + update({ data }) + digest()。

## 原因

已观察到 Md.update 传入零长度 DataBlob 时运行期抛错（build context fail.），而源端对空串照常返回摘要；空字段在目标中断整个调用。只调用 digest() 不调用 update 是否可行尚未在干净构建上验证。

## 做法

1. 输入为空时不调用 update，直接返回该算法对空输入的标准摘要（SHA-256("") = e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855）；非空才 update 后 digest。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-02b09ca8c5fcae827ebd](../../../store/cases/case-02b09ca8c5fcae827ebd/032f286c325932d0ca0005749aa6085360442e75a0328b49ec451c7cc8645020.json) · 结论：diagnosis, recommendation:3
  卡片版本：`032f286c325932d0ca0005749aa6085360442e75a0328b49ec451c7cc8645020`

# 跳过清单和 unmapped 登记

agent 会看到什么：skip-list 或 resource-mapping 里写「平台无对等、降级」「跳过（unmapped）」「由某 feature 处理」，没有检索记录，也没有逐键登记被跳过的值和承接方

## 规矩

- rule-ded6f766a0b6｜跳过清单登记「平台无对等、降级」前先检索 SDK，写明检索词和命中接口｜读到：源端功能依赖系统级能力，源码自带版本门槛和不支持时的回退分支；写错：skip-list 行写「<能力> | 平台无对等 | HMOS 无 X API；降级为固定方案」，没有检索词、命中的 d.ts 或检索为空的记录
- rule-47ed0a4b16bb｜跳过宽度限定目录时，逐键登记被覆盖的值为运行时断点并写明承接方｜读到：源工程 res 下有 values-w<N>dp、values-sw<N>dp、values-h<N>dp 这类尺寸限定目录，里面的 dimens.xml 覆盖了 values/dimens.xml 的同名键；转换规则写这类目录 skip entire directory, mark as unmapped；写错：resource-mapping 里只写该目录“跳过（unmapped）”或“由某 feature 处理”，被点名的 feature spec 里并没有对应条目；placeholder-registry 里没有这项运行时断点，回执也没提
- rule-b9bf54e31739｜登记「无 ArkUI 等价」降级前，写明在 SDK .d.ts 里搜过的枚举或方法和结论｜读到：源端用了某种绘制能力（如 BlendMode 混合、渐变描边、渐变着色），实现者打算降级；写错：降级登记写了「无 ArkUI 等价」「ArkUI 不支持…」，没写查过哪个声明文件、搜了什么；或者「保留」裁决照搬组件注释里的降级理由
- rule-90bd89d7ba47｜子代理标为「存疑」的平台能力结论，写进 skip-list 或 HARD-DIV 前先复核证据｜读到：子代理回执把「平台无对等」列为存疑项、供后续定夺；写错：skip-list 或 feature-index 写成「HARD-DIV：平台无…」的定论，没有检索证据

# 核 SDK d.ts 时读字段的 doc 行与语义段，不只 grep 签名

ID：`lesson-5ebfd81b0d3ff8f55999` · 版本：1

[本主题](index.md)

## 何时使用

规格提取或界面实现阶段，用 grep/sed 在 SDK d.ts 里核对某个 ArkUI 属性、接口字段或方法是否可用、单位/语义是什么时

## 适用情境

grep 命令只保留签名行（`radius: number | Resource;`、`lineHeight(value: …)`、`blendMode(…)`、`BorderOptions`），紧邻的 `/** … unit is px */` 或语义描述被过滤掉；随后据此写契约或定 HARD。

## 原因

四张卡的偏差起点都伴随「只核签名」：ShadowOptions 的 px 单位行被过滤（dp 当 px）；text.d.ts 只核到 lineHeight 签名存在（单行撑高）；blendMode 只读到一句未定义范围的文档（离屏混合目标误判）；BorderOptions 只核 color/width 类型（描边计入测量）。同名 API 存在不等于行为等价。

## 做法

1. grep 命中签名后用 sed -n 打出其前后 10–20 行 doc，把单位、作用范围、默认行为抄进契约理由；写 `.blendMode(…, OFFSCREEN)` 这类语义型属性前读 common.d.ts 的语义段。
2. 契约理由里禁止只写「依据 d.ts 存在同名方法」；必须能回答单位是什么、对单行/无定尺容器/兄弟节点各自行为如何。

## 检查

- 回看 spec/映射文档里每条「依据 xxx.d.ts」的理由，能否指到 doc 行而不只是签名行。

## 来源（按需复核）

经验是有适用范围的历史建议。核查来源时同时看结论与 unknown；来源卡未随阅读包复制。

- [case-0e3ff99e6b2aa8afcfff](../../../store/cases/case-0e3ff99e6b2aa8afcfff/b2cd27b13b55dc1007d5bd4cfcc7bc3eb62178557df5bf1e801f6b2960507c36.json) · 结论：recommendation:4
  卡片版本：`b2cd27b13b55dc1007d5bd4cfcc7bc3eb62178557df5bf1e801f6b2960507c36`
- [case-4056358e68946ac061c6](../../../store/cases/case-4056358e68946ac061c6/c064fce84bd61cbdd2a7d203b85e576c31033aba00f2dd902f4e42414cad012d.json) · 结论：recommendation:1
  卡片版本：`c064fce84bd61cbdd2a7d203b85e576c31033aba00f2dd902f4e42414cad012d`
- [case-75329cae60986f74dc43](../../../store/cases/case-75329cae60986f74dc43/e05464cbccdf6181891a9fd2ddf2bbc2143a88e5f4fc4dcc3b1be803917b20cf.json) · 结论：recommendation:1
  卡片版本：`e05464cbccdf6181891a9fd2ddf2bbc2143a88e5f4fc4dcc3b1be803917b20cf`
- [case-77c4d0c99ad4a6486b79](../../../store/cases/case-77c4d0c99ad4a6486b79/286ff5c4b52e33ee2cc428e7db64dedfa354a34e6bdf3ca4a9c44631b01ceffb.json) · 结论：recommendation:2
  卡片版本：`286ff5c4b52e33ee2cc428e7db64dedfa354a34e6bdf3ca4a9c44631b01ceffb`

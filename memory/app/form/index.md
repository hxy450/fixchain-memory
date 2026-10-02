# app/form

服务卡片：卡片页可用的事件与写法限制（@form 标注、V1 卡片页的派生值）、由 FormExtensionAbility 取实际尺寸并派生布局档位，以及 form_config 规格、缩放与刷新从源 appwidget-provider 换算

[上一级](../index.md)

## 本级经验

- [form_config 的规格、默认规格、缩放与刷新从源 appwidget-provider 换算，不凭默认档位填写](lesson-bc48518f40742add0054.lesson.md)
  - 时机：编排或服务卡片实现阶段，写 form_config 的 supportDimensions、defaultDimension、resizable、刷新与预览配置时
  - 情境：源端 appwidget-provider 与 dimens 声明目标格数、最小/最大尺寸、可调尺寸、缩放模式和刷新周期，决策账本可能已批准静态预览；上游回报只说“具体档位待回填”。
- [服务卡片按实际宽高选布局：由 FormExtensionAbility 取尺寸下发，V1 卡片页的派生值写成普通方法](lesson-7ad5a7d149de5bcec7da.lesson.md)
  - 时机：服务卡片实现阶段，卡片需要按实际宽高选择布局档位，或在 V1 @Entry 卡片页里由尺寸等状态派生布局值时
  - 情境：源端 Glance AppWidget 用 SizeMode.Exact/LocalSize 按卡片实际宽高选布局（宽度断点、按高度显示标题栏等）；目标为 ArkTS 服务卡片（V1 卡片页 + FormExtensionAbility + form_config 离散规格），实现者准备在卡片页用通用尺寸事件取宽高，或只按 FormDimension 档位一档对一形态。

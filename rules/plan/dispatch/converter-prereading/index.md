# 页面转换派工的前置必读

agent 会看到什么：页面转换派工里的前置 skill 清单和要点名的错误模式：源端带状态参数的子控件要转成 @Builder 复用，或本会话刚出现过 ArkTS 组件语法报错（';' expected、Only UI component syntax）

## 规矩

- rule-07c1503c9253｜派发页面转换器时，前置必读清单纳入 @Builder 复用一节（含动态状态不能作值参）｜读到：页面转换任务要把源端带状态参数的子控件转成 ArkUI 复用写法；写错：派工的前置 skill 清单只有 ui-graph-query、ui-alignment、design-tokens-extractor、navigation-builder 这类，没有 arkts-component-builder 的「@Builder / @Styles / @Extend 复用」一节
- rule-f41a3127a67e｜本会话刚出现过 ArkTS 语法报错时，派同类页面的派工点名该错误模式并要求先读语法约束｜读到：本会话刚出现过同类页面的 ArkTS 编译报错（';' expected、Only UI component syntax can be written here、does not meet UI component syntax）；写错：派同类页面实现的派工没有点名这类错误模式，没要求实现者先读组件语法约束（arkts-component-builder），也没要求交付后按该模式复查
- rule-766cb9c0ad4c｜派 V2 界面返修或重写任务时，把响应式硬规矩写进派工说明，不只说技能可用｜读到：目标工程用 @ComponentV2/@Local/@Trace，工程技能里写有「动态状态不能作 @Builder 值参」「LazyForEach 不响应数据源对象重赋值」；写错：返修或重写的派工说明只有「某类技能可用」一句，没写这两条规矩，也没要求执行者先读对应小节并在报告里确认

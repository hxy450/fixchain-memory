# app/identity

应用身份与启动资源：包名、分层图标、启动窗底色与模板残留

[上一级](../index.md)

## 本级经验

- [启动窗底色按源主题的冷启动窗口背景对齐，并清理模板限定符资源](lesson-2358300fc802fd78c2fd.lesson.md)
  - 时机：资源前置与应用身份落地阶段，合并模板element资源、确定启动窗底色和限定符目录时
  - 情境：目标由DevEco模板初始化，module.json5用$color:start_window_background设启动窗底色，模板还自带dark/element/color.json；源主题未覆写windowBackground，源端可能没有values-night。
- [延后迁移bundleName前先核延后前提，不把模板包名留到交付](lesson-97d56014f8646e59ec46.lesson.md)
  - 时机：执行阶段落地应用身份时，决定app.json5的bundleName迁移为安卓applicationId还是保留占位时
  - 情境：目标工程由DevEco模板生成，bundleName仍为模板默认值；源端有明确applicationId；流水线规则要求开发期跳过bundleName（理由是与签名或上架绑定）。
  - 例外：工程已配置签名且当前阶段确实不能改包名时，换成本工程唯一的占位值，并在台账登记落地时机
- [旧式单层启动图标转分层图标时两层同画布，主体缩入前景安全区](lesson-a2f089bf04387057c2ab.lesson.md)
  - 时机：资源与应用身份迁移阶段，为只有单层ic_launcher的源工程生成AppScope分层图标的前景层与背景层时
  - 情境：源端只有mipmap-*dpi/ic_launcher.png单层旧式图标（无自适应图标），图标主体接近铺满位图；目标以layered_image引用foreground/background两层，脚手架两层为同尺寸画布。

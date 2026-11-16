# dark 目录 color.json 对页面色键的覆盖

agent 会看到什么：验收要求页面配色随深浅资源限定符切换，页面和共享常量引用 $r('app.color.…')；dark/element/color.json 的键少于 base 里页面用到的 app.color 键（自检输出 base N / dark M），交付说明写「无差异」、decision_gaps 为空

## 规矩

- rule-7042cdc71471｜dark 的 color.json 要覆盖页面引用的全部 app.color 键，缺口写进 decision_gaps｜读到：验收条目要求页面配色随深浅资源限定符切换；页面和共享常量里引用 $r('app.color.…')；写错：dark/element/color.json 的键少于 base/element/color.json 里页面用到的 app.color 键（自检输出如 base 15 / dark 8），交付说明 Spec Gap 写「无差异」、decision_gaps 为空

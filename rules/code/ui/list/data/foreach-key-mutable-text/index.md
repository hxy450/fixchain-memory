# ForEach 键函数和项里随语言、状态变的文案

agent 会看到什么：读到列表项文案改成渲染期按语言或别的 @Trace 状态经 t(key) 取值、切换时整体替换数组；产物里 ForEach / LazyForEach / Repeat 的 keyGenerator 只返回恒定 id（如 (opt) => opt.value），项内 Text(opt.label) 显示可变文案

## 规矩

- rule-bc24a5c19095｜列表项文案随语言或状态变化时，ForEach 的 keyGenerator 要把可变显示字段编进 key｜读到：列表项显示的文案改成渲染期按语言（或其他 `@Trace` 状态）经 `t(key)` 取值，数组在切换时整体替换；写错：`ForEach(options, …, (opt) => opt.value)` 一类只返回恒定 id 的 keyGenerator，项内 `Text(opt.label)` 显示可变文案

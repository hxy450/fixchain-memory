# 整套迁移的 Markdown 渲染库（Markwon 插件链）

agent 会看到什么：读到源端用 Markwon（以 commonmark 解析为底座）加若干插件渲染 Markdown，Markwon.builder(context).usePlugin(...) 插件链；规格的实现映射写「各插件可观察效果逐一等价」，AC 只覆盖插件和表格、删除线、HTML，没有嵌套列表、惰性续行、松紧列表、引用内块这些 CommonMark 核心语法的契约

## 规矩

- rule-de409598b4ba｜迁移整套第三方 Markdown 渲染库时，规格契约覆盖 CommonMark 核心语法并给可断言样例 AC｜读到：源端用 Markwon（以 commonmark 解析为底座）加若干插件渲染 Markdown，Markwon.builder(context).usePlugin(...) 插件链；写错：规格的实现映射写「行为目标=各插件可观察效果逐一等价」，AC 只覆盖插件和表格/删除线/HTML，没有嵌套列表、惰性续行、松紧列表、引用内块、行内元素按原文顺序的契约；复杂度按插件代码量判为 simple

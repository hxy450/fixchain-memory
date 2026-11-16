# 迁入 HAR 的页面的资源闭包

agent 会看到什么：页面源码里有 $r('app.string/media/color.X') 或 getStringByNameSync 这类按名引用，迁移范围表或计划只列页面、VM、Service，没列 element 条目和 media 文件

## 规矩

- rule-d3237a502567｜页面迁入 HAR 或在 feature 间移动时，迁移清单列上页面的资源闭包｜读到：页面源码里有 `$r('app.string/media/color.X')`，或用 getStringByNameSync / getMediaByNameSync / 封装的按名取字符串函数引用资源；写错：迁移范围表或计划只列页面、VM、模型、Service、Repository，没列 resources/*/element 条目和 media 文件；资源清单只按 app.(string|media|color).X 静态写法扫描，漏掉按名引用的字面量

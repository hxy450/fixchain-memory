# Kotlin / Java 字符串和正则函数的语义

agent 会看到什么：读到 Kotlin / Java 源码的 contains / startsWith / endsWith（传没传 ignoreCase）、lineSequence() / lines()、replaceFirst / replace，或 Pattern 正则里的 \s、\p{L} 和交替替换；产物里 TS 自加的 toLowerCase 归一、split('\n')、只换首个的 String.replace、手写的 ASCII 字符类或拆成两遍的替换

## 规矩

- rule-13ca2e2e51cd｜contains/endsWith/startsWith 没传 ignoreCase 时，目标保持大小写敏感｜读到：Kotlin 源码里 `contains("…")`、`endsWith(".ext")`、`startsWith("…")` 没有传 `ignoreCase = true`，前面也没有 `lowercase()`；写错：目标端写成 `s.toLowerCase().indexOf('…') >= 0`、`name.toLowerCase().endsWith('.ext')`，自行加了大小写归一
- rule-93ad0f7e3c8c｜源码用 lineSequence()/lines() 分行时，目标按 \r\n、\n、\r 三种行尾分行｜读到：Kotlin 源码对文本调用 `lineSequence()` 或 `lines()`；写错：目标端写成 `split('\n')`，\r\n 的行尾留下 \r、只用 \r 分行的文本不分行
- rule-babeec36fa1f｜Kotlin replaceFirst(…, true) 只换首个且忽略大小写，replace 换全部｜读到：Kotlin 源码 url.startsWith("http://", true) 后 replaceFirst("http", "https", true)，或 String.replace("www.", "") 一类替换；写错：目标写成 'h' + url.substring(1) 这类结果等于原串的拼接，或用 String.replace('www.', '') 只替换了第一个
- rule-5db8531b77b9｜Android 正则走 ICU：\s 是 White_Space、\p{L} 不含 \p{M}、交替替换单遍｜读到：源码正则含 \s（如 s.matches("\\s")、".*(\\s|^)tag(\\s|$).*"），或 replaceAll("(" + Pattern.quote(a) + "|" + Pattern.quote(b) + ")", "")；写错：目标写 /[ \t\n\f\r]/ 并注释「Java \s 仅 ASCII 空白」，字母类写 [\p{L}\p{M}]，或把交替替换拆成两遍 split / join

# 资源

派工、交接、资源映射报告或收口回报涉及 strings.xml / string.json、colors.xml / color.json、$r 令牌、多语言、图标和 SVG 资源的来源与转换结果时

## 触发族

- [字符串资源在派工和交接里的写法](string-resource-handoff/index.md)（7 条）：派工、交接或转换报告涉及把源端字符串资源（strings.xml、@string/app_name、android:text 的字面量、Res.string 的键）带到目标 string.json：键和解析后的值、值语义、缺的条目
- [颜色资源的转换结果和令牌](color-resources/index.md)（3 条）：资源阶段或页面转换涉及颜色资源（colors.xml → color.json、$r('app.color.*') 令牌）：转换脚本只打印 unresolved 总数、已完成的 color.json 被标「勿重做」、令牌缺失被换成值不同的已有令牌，报告或派工照常宣布 PASS
- [交付说明里的图标资源来源](icon-sources/index.md)（1 条）：规格里有元素→资源表、计划写明资源从 Android 原图提取，交付说明写「项目中已有的原图标并统一着色」，没有逐项列出资源和来源
- [转换器造成的共享资源缺陷](converter-defects/index.md)（1 条）：页面 worker 判定共享资源错在转换器（如 converter used dp size as viewBox），回执只写「修复 N 处 SVG viewBox 错配」，编排记录里记成顺手修复，没有全量审计
- [资源映射报告里的多语言取舍](locale-conflict/index.md)（1 条）：规格写「默认文案为英文、不擅自翻译」而资源转换 skill 要求至少生成 2 套语言，资源映射报告把非 base 语言记成显式译文，只报键一致、没写冲突
- [收口回报里的图标项](icon-closing/index.md)（2 条）：资源迁移或收口回报写着 AppScope 的 app.json5 icon 仍是脚手架 $media:app_icon 并记为「非阻断」，或跑了会改写源码的 icon-sizing 自愈脚本却只报 findings 计数

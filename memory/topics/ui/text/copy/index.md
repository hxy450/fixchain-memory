# ui/text/copy

可见文案的来源：沿资源引用链取逐字值、静态页文案取自 XML、代码格式化文案建参数化资源、语言目录按源生成。

[上一级](../index.md)

## 本级经验

- [代码内经资源管理器取值传 $r().id](lesson-22432022455bff6f849b.lesson.md) · 阶段：execute · 信号：getStringSync, getStringArrayValueSync, getIntPluralStringValueSync, getPluralStringValueSync
- [代码格式化的固定措辞文案建参数化资源，$r 传参不写模板串](lesson-d442eb6e9aab4d77db18.lesson.md) · 阶段：execute · 信号：SimpleDateFormat, String.format, $r('app.string, string.json
- [可见文案沿引用链取 strings.xml 逐字值，非枚举名](lesson-31ab9f59945e5f0259ea.lesson.md) · 阶段：plan/execute · 信号：strings.xml, @string/, stringResource
- [字符串全集取含依赖库的合并资源表，不只模块 res](lesson-fe295e164208c44e9116.lesson.md) · 阶段：plan/execute · 信号：apktool, aapt2, values-*, ~/.gradle/caches
- [字符串按 aapt2 语义转值：折空白、剥引号](lesson-f88b9c824280ce239dea.lesson.md) · 阶段：execute · 信号：strings.xml, string.json, aapt2, el.text
- [系统文案建专属键补各语言框架译文](lesson-ff19b09146b57d0f91a8.lesson.md) · 阶段：execute · 信号：android.R.string.ok, @android:string/cancel, android.R.string, positiveButtonText
- [缺文案键新建专属键并交接原值，不借近义](lesson-4567f9f77f4280ec1747.lesson.md) · 阶段：execute/converge · 信号：string.json, strings.xml, android:text, $r('app.string.
- [语言目录按源 values-* 全集与粒度镜像](lesson-b58df29f032cc6a8c9d6.lesson.md) · 阶段：spec/execute · 信号：values-zh, values-zh-rTW, strings.xml, zh_CN
- [说明类静态页按源 XML 逐卡迁移，文案逐字取自源布局](lesson-0197307e63e8d848ba02.lesson.md) · 阶段：execute · 信号：@drawable, android:text, string.json, $r('app.string

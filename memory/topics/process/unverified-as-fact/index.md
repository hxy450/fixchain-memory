# process/unverified-as-fact

把生成期无法核验的推测、自拟值或假设写成硬性结论、期望值或已实现项

[上一级](../index.md)

## 本级经验

- [替换共享渲染公式时分开已核与假设，以正确场景作回归基线](lesson-cf92f65492e41a03ed8a.lesson.md) · 阶段：repair · 信号：lineHeight, fontSize
- [点击无响应先设备复现定位，未上机结论标未验证](lesson-afae8d13e00941efe808.lesson.md) · 阶段：verify/repair/converge · 信号：hitTestBehavior, uitest uiInput click, dumpLayout, hdc shell
- [结论先查本机 SDK 与依赖源，查不到才标置信度](lesson-c0f990ea57a901951ba8.lesson.md) · 阶段：spec/execute · 信号：HARD, dp, .gitmodules, ?android:attr
- [规格所需值上游缺失时回源码补或标待核，不自拟](lesson-77ca67f164d77ec63cda.lesson.md) · 阶段：spec · 信号：api-inventory.json, auth_model, common.md, raw_apis.json
- [颜色差异立单用像素均值和源端算式给期望值](lesson-aae5f345ed2ced099757.lesson.md) · 阶段：verify · 信号：PNG, blendMode, ColorFilter

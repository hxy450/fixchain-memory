# process/claimed-without-receipt

凭文本形式的调用、部分输出、过期构建或自动脚本结果宣告写入与完成，缺少真实回执核验

[上一级](../index.md)

## 本级经验

- [sed/perl 改含 $r 的片段用单引号并读回](lesson-6dae0bf2657b0e339742.lesson.md) · 阶段：execute/repair · 信号：perl -pi, sed -i, $r(, app.float
- [写文件以执行回执为准，覆盖入口页后内容断言读回](lesson-776ed5eb216833c6b002.lesson.md) · 阶段：execute/verify · 信号：loadContent, Hello World, RelativeContainer, apply_patch
- [功能对齐以代码落点为准，空回调不算实现](lesson-9147be4d87153de9c5b6.lesson.md) · 阶段：execute/verify · 信号：onClick, JSON.stringify, NavPathStack, onEventMainThread
- [编译按完整 ERROR 列表判定，失败只记 FAIL](lesson-7426a20525e52e34c2e7.lesson.md) · 阶段：verify/repair · 信号：COMPILE RESULT, BUILD SUCCESSFUL, BUILD FAILED, hvigor
- [缺 hvigorw 时用工具自带构建，文本契约不算编译](lesson-25bc0b7518d335a947d6.lesson.md) · 阶段：execute/verify/repair · 信号：hvigorw, assembleHap, command-line-tools/bin/hvigorw, CompileArkTS
- [自愈脚本改写 .ets 后先审 diff，异常尺寸回滚](lesson-bdb97da6a6eb8d68435f.lesson.md) · 阶段：verify/converge · 信号：icon-sizing, .width, .height, Image

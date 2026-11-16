# Compose 未定尺寸的 Surface / Box 的尺寸与描边

agent 会看到什么：读过的 Compose 源码里 Surface / Box 只加 clickable、clip、border、background，有没有 Modifier.size 决定它的尺寸；交回的按钮自加了 16 或套了 40、48vp，或在尺寸由内容决定的 Stack / Column 上直接写 .border(...)

## 规矩

- rule-612361811947｜Compose Surface/Box 没设尺寸时，按钮尺寸等于内容尺寸，不自加 16 或套 40/48｜读到：Compose Surface / Box 只加 clickable、clip、border、background，没有 size / width / height，内容是没写 size 的 Icon；调用方只传 Modifier.align 这类不改尺寸的修饰；写错：外层 .width(...) / .height(...) 写成图标尺寸加 16，或套用 IconButton 的 40、48vp
- rule-46edea01a389｜没有显式宽高的容器不直接写 .border()，改用按测得尺寸定位的覆盖层画描边｜读到：源组件用 Compose Modifier.border(BorderStroke, shape) 在已定尺的盒内侧描边；写错：目标在没有 width / height、尺寸由内容决定的 Stack 或 Column 上直接写 .border(...)

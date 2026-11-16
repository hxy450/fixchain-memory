# 外观全来自第三方 UI 库默认样式的组件

agent 会看到什么：读到源组件只引入第三方库的默认样式（如 swiper/css/navigation、swiper/css/pagination），没有主题变量或样式覆盖；实现映射只写「ArkTS Swiper + indicator + 自定义左右导航按钮」这类行为描述，没有库名、版本、默认颜色尺寸形状或样式出处

## 规矩

- rule-aed9b0b5bf89｜源控件外观全来自第三方库默认时，规格的实现映射写明库名、版本和默认视觉值｜读到：源组件只引入第三方库默认 CSS（如 swiper/css/navigation、swiper/css/pagination），没有主题变量或样式覆盖；写错：实现映射只写「ArkTS Swiper + indicator（可点跳页）+ 自定义左右导航按钮」这类行为描述，没有库名、版本、默认颜色尺寸形状或 CSS 出处

# 文本与文案

源端有 TextView、Compose Text / TextStyle、strings.xml、getString / stringResource、String.format、DecimalFormat、Html.fromHtml、Spannable、contentDescription，目标端有 Text、Span、$r('app.string.…')、fontSize、lineHeight、maxLines、accessibilityText 时

## 子主题

- [界面文案与取串](copy/index.md)（30 条）：源端有 strings.xml、R.string / Res.string、android:text、getString / stringResource（带或不带格式参数）、i18next 的 t('…')、contentDescription，目标端有 Text('…') 字面量、$r('app.string.…')、resourceManager.getStringSync、模板串或拼接出的文案、.accessibilityText 时
- [字号、字体与文字外观](font/index.md)（16 条）：源端有 TextView / EditText 的 textSize、textColor、textAppearance、fontFamily、shadow*（或没写、由主题决定），由 dp 乘文字倍率算出的字号，或 Compose MaterialTheme.typography 的命名样式、FontWeight、FontFamily(Font(R.font…))，目标端有 Text / TextInput 的 fontSize、fontColor、fontWeight、fontFamily、textShadow、registerFont 时
- [行高、行数与省略](lines/index.md)（21 条）：源端有 TextView 的 android:lineHeight、includeFontPadding、maxLines / lines / ellipsize（或都没写）、可能为空的 wrap_content 文本，或 Compose TextStyle 的 lineHeight、Text 的 maxLines / overflow，目标端有 Text 的 .lineHeight、.lineSpacing、maxLines、minLines、textOverflow，或按一行高度算的容器高度和相邻元素定位时
- [应用语言与区域](locale/index.md)（7 条）：源端有 AppCompatDelegate.setApplicationLocales / getApplicationLocales、supported_locales、Locale.getDisplayName、按设备语言主标签映射语言码、lowercase(Locale.ROOT) 或按 locale 的 toUpperCase / textAllCaps，目标端有 i18n.System.setAppPreferredLanguage、getSystemLanguage / getFirstPreferredLanguage、getConfigurationSync().locale、toLocaleUpperCase 时
- [富文本、链接与标记](rich-text/index.md)（12 条）：源端有 SpannableString.setSpan、ForegroundColorSpan、ClickableSpan / URLSpan、LinkMovementMethod、Linkify.addLinks、Html.fromHtml、Compose buildAnnotatedString / LinkAnnotation，或用 react-markdown 渲染 Markdown，目标端有 Span、RichEditor、TextController、Text 上的手势和自写的链接或标记解析时
- [数字、日期与数据值的显示格式](value-format/index.md)（20 条）：源端在显示前用 String.format、NumberFormat / DecimalFormat、getCurrencyInstance、Formatter.formatShortFileSize、DateFormat、PrettyTime、DateUtils.formatDateTime，或用 when / switch 穷举表、转换函数把数据值转成显示文本，目标端有 intl.NumberFormat / DateTimeFormat / RelativeTimeFormat、toFixed、toLocaleString、toString()、自写的格式化和分档函数时

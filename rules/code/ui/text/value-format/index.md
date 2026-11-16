# 数字、日期与数据值的显示格式

源端在显示前用 String.format、NumberFormat / DecimalFormat、getCurrencyInstance、Formatter.formatShortFileSize、DateFormat、PrettyTime、DateUtils.formatDateTime，或用 when / switch 穷举表、转换函数把数据值转成显示文本，目标端有 intl.NumberFormat / DateTimeFormat / RelativeTimeFormat、toFixed、toLocaleString、toString()、自写的格式化和分档函数时

## 触发族

- [数据值转显示文本的转换和格式化](display-text-conversion/index.md)（6 条）：读到源端显示前用 when / switch 穷举表、转换函数、带默认参数的格式化函数，或把 Float 直接放进字符串；产物里直接 toString()、.join、原值透传、模板串，或另写的格式化函数默认值和源端不同
- [平台格式化器的数字、金额、日期格式化](number-format/index.md)（12 条）：读到源端用 String.format、NumberFormat / DecimalFormat、getCurrencyInstance、Formatter.formatShortFileSize、DateFormat 格式化数字、金额、文件大小和日期，常不显式传 Locale；产物里写成无参 intl.NumberFormat、toFixed、toLocaleString、手拼串或固定格式，区域、币种、舍入、进位和精度与源端不同
- [PrettyTime、DateUtils.formatDateTime 一类的相对时间和日期显示](relative-time-library/index.md)（2 条）：读到源端用 PrettyTime（format、formatDuration，setLocale）或 DateUtils.formatDateTime 的 FORMAT_* 标志生成相对时间和日期文案；产物里用 intl.RelativeTimeFormat / intl.DateTimeFormat 配自定阈值和取整，或写成固定英文的分档函数，注释称「库默认粒度」

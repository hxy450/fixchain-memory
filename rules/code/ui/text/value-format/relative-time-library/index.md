# PrettyTime、DateUtils.formatDateTime 一类的相对时间和日期显示

agent 会看到什么：读到源端用 PrettyTime（format、formatDuration，setLocale）或 DateUtils.formatDateTime 的 FORMAT_* 标志生成相对时间和日期文案；产物里用 intl.RelativeTimeFormat / intl.DateTimeFormat 配自定阈值和取整，或写成固定英文的分档函数，注释称「库默认粒度」

## 规矩

- rule-9bb047aa67aa｜用系统 i18n / intl 替代有自有阈值和模板的库时，移植算法和资源，不自定阈值冒充库默认｜读到：源端 new PrettyTime(); pt.setLocale(locale); pt.format(date)；写错：目标用 intl.RelativeTimeFormat(…, { numeric: 'auto' }) 配自定阈值（秒、天、周、月、Math.round），注释写「prettytime 默认粒度」
- rule-71fc32f8a730｜源函数只是委托第三方格式化库时，按库的实际行为移植并对拍，做不到就登记占位｜读到：源端共享工具函数体只是 PrettyTime(Locale.getDefault()).formatDuration(...)，另有只在 en 生效的缩写分支、纯数字时回退英文；写错：目标写成固定英文的相对时间：不到 1 分钟返回固定词、按 30 / 365 天分档、Math.round 或 floor 凭记忆取整、不看 locale；没有登记占位或决策缺口

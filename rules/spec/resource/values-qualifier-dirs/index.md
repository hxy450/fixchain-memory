# res 下的 values-* 语言和屏宽目录

agent 会看到什么：读过的源工程 res 下有多个 values-<语言> 目录或 values-w<N>dp / values-sw<N>dp 目录，自绘 View 用 getString 取文案画到画布；交回的规格自设只迁部分语言、漏了屏宽覆盖的 dimen，或语言切换的验收只看代码引用

## 规矩

- rule-83d0d78789e6｜规格登记语言资源范围时按源 res 下全部 values-* 目录，不自设只迁双语的默认值｜读到：源工程 res/ 下有多个 values-xx 语言目录（如 values-es、values-zh-rTW），应用内按 supported_locales 提供语言切换；写错：规格全局约定或决策台账写「默认迁 values + values-zh」「其余语言 fallback base，行为可接受」，没有用户或任务的裁剪来源
- rule-c9f3f2f63060｜规格盘点 values-* 时，宽度限定目录覆盖的 dimen 写进全局约定并指派运行时判定｜读到：源工程 res 下有 values-w<N>dp 或 values-sw<N>dp 目录，覆盖了布局共用的 @dimen；源码理解笔记或设计文档里写了宽屏下的覆盖值；写错：ui-manifest 只把宽度限定目录记成“非语言目录”，全局约定里没有被覆盖的 dimen；引用它的页面 meta.json 的 style_sources 只列 values/dimens.xml；feature-base 和各页 spec 里没有宽度断点
- rule-02a9810e7088｜「文案随语言切换」的验收写成两种语言配置下对比画布与组件文本，不只看代码引用｜读到：安卓自绘 View 用 getResources().getString 取文案画到画布上，同一屏还有普通控件的文案；写错：「文案随语言切换」的验收条目或核验记录只看代码里有没有引用 $r / getStringSync，或写「无应用内语言切换，无需 setPreferredLanguage」就判通过
- rule-2bd4e8fc786e｜规格登记 sw 限定目录覆盖时，写明判定量是屏幕短边 min(宽,高)、与方向无关，再叠方向｜读到：源工程有 values-sw<N>dp 或 values-sw<N>dp-land 限定目录里的覆盖值（注释常写给平板用）；写错：规格只写“横屏 + 最小宽度≥N”或“断点宽 N vp + 横屏”，没写明比较的是设备屏幕短边 min(宽,高)、与方向无关，也没举手机横屏不命中的例子

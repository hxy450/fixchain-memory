# 控件形制来自三方库时派工给的查值来源

agent 会看到什么：规格或映射登记了三方库名和版本（如 material-dialogs → CustomDialog、preference-ktx 运行时构建），控件形制来自库资源、项目 res/ 里没有；派工只列了安卓源码路径，没写库 AAR 在 Gradle 缓存里的位置，也没提示解包查 values 和 layout

## 规矩

- rule-0f31172653a2｜派工给出安卓源码路径而控件形制来自三方库时，一并给出库 AAR 的缓存位置和解包查值的提示｜读到：规格或映射里登记了三方库名和版本（如 material-dialogs → CustomDialog、preference-ktx 运行时构建），控件形制来自库资源、项目 res/ 里没有；写错：派工只列了安卓源码路径，没写该库 AAR 在 Gradle 缓存里的位置，也没提示可以解包查 values 和 layout 的真值

# 导航目的地的 argument 声明

agent 会看到什么：导航图 XML 目的地下的 <argument>（app:argType、app:nullable、android:defaultValue）和 Fragment 的 requireArguments() 取参；分页规格里的页面入参一项

## 规矩

- rule-f91f610cc4f4｜导航目的地声明了 <argument> 时，分页规格写明页面入参的名称、类型、可空和取参处｜读到：导航图 XML 的目的地下有 <argument android:name=… app:argType=…>（可带 app:nullable、android:defaultValue），Fragment 用 requireArguments() / arguments 读取；写错：分页规格没有「页面入参 / 取参方式」一项；导航图一节只留起始目的地、底部导航和深链占位（如 {参数名}），丢了各目的地的 argument 声明

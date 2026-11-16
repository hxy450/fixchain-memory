# 界面文案与取串

源端有 strings.xml、R.string / Res.string、android:text、getString / stringResource（带或不带格式参数）、i18next 的 t('…')、contentDescription，目标端有 Text('…') 字面量、$r('app.string.…')、resourceManager.getStringSync、模板串或拼接出的文案、.accessibilityText 时

## 触发族

- [组件上的 .accessibilityText](accessibility-text/index.md)（3 条）：读到源端的 android:contentDescription、Icon 的 contentDescription = null，或规格里 string | Resource 的文案字段，交回的代码给组件写了 .accessibilityText(...)：传的值是什么类型、文案从哪来
- [可见文案的逐字取值](ui-strings/index.md)（9 条）：源端 strings.xml、R.string / Res.string、android:text 和偏好对话框给出的界面文案，对应目标 Text(...) 的字面量或 $r('app.string.…') 引用的是哪一条、值和源端是否逐字一致，以及空值时回退的占位文案
- [带格式参数的文案](formatted-strings/index.md)（7 条）：源端 getString / stringResource 带实参、android:summary 的 %s，或代码里 String.format / SimpleDateFormat / 拼接出的文案，对应目标 $r('app.string.…', 参数…)、getStringSync(id, ...args)、模板字符串、+ 拼接和 replace 插入
- [代码里经 resourceManager 取文案](resource-manager-strings/index.md)（8 条）：目标代码里手里是 $r(…)、Resource 或 ResourceStr 而要的是 string 的地方：resourceManager.getStringSync / getStringByNameSync / getStringArrayValueSync 的传参、getHostContext() 取上下文、typeof 收窄，或构建报 Resource 不能赋给 string；源端对应 getString、getResources().getString
- [翻译键 t() 的文案和 FWD-REF 过渡](i18n-t-key/index.md)（3 条）：源页面文案来自运行期翻译键 t('…')（i18next、useTranslation），目标页面里有固定语言的 Text('…') 字面量、指向翻译服务的 FWD-REF 标记，或头注释里拿 D- 编号给字面量过渡做依据

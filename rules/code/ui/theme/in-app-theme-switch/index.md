# 应用内切换主题和深色模式

agent 会看到什么：读到源端按偏好 setTheme、recreate、AppCompatDelegate.setDefaultNightMode 切换浅色 / 深色主题；产物里 setColorMode 的调用时机、getColorSync 命令式取色和系统栏内容色

## 规矩

- rule-665c8b7f0b82｜冷启动恢复持久化主题放在 EntryAbility.onCreate 的同步路径，loadContent 前完成｜读到：入口 Activity.onCreate 里 super.onCreate(...) 之前按 SharedPreferences 调 setTheme(...) 设 DayNight 主题；写错：恢复函数写成 async …: Promise<void>，内部 await preferences.getPreferences(...) 后才 setColorMode，EntryAbility.onCreate 里不等待地调用它
- rule-294e34d3fd6e｜应用内用 setColorMode 切主题时，命令式取色改用覆写 colorMode 的资源管理器｜读到：源端换主题靠 Activity 重建（ActivityCompat.recreate / Activity.recreate），主题在界面创建时按用户偏好 setTheme；写错：目标端只调用 ApplicationContext.setColorMode，注释断言「全部 $r 资源随 mode 即时重解析，等价 recreate」；画布、HTML 样式等仍用 context.resourceManager.getColorSync 取色，应用内选深色而系统为浅色时取到浅色值
- rule-8cc442c2a52d｜系统栏内容色按生效的 colorMode 计算（亮 #000000 / 暗 #FFFFFF），并在配置变化时重设｜读到：源应用 styles.xml 里有浅色 / 深色 / 纯黑几套主题，换主题时状态栏图标随主题变；写错：setWindowSystemBarProperties({ statusBarContentColor: '#000000', navigationBarContentColor: '#000000' }) 写死一个颜色，注释写「深色模式由主题管线后续处理」

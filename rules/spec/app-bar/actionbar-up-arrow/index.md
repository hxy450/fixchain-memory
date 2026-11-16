# 带窗口 ActionBar 的页面的 Up 箭头

agent 会看到什么：读到源 Activity 用带 ActionBar 的 AppCompat 主题、Manifest 有 parentActivityName、onOptionsItemSelected 处理 android.R.id.home；页面规格的导航表写「ActionBar Up（若有）」或只按 setDisplayHomeAsUpEnabled 判断

## 规矩

- rule-9c4ef9ccadc3｜带 ActionBar 的页面规格写定 Up 箭头显不显示和依据，不写「若有」｜读到：源 Activity 用带窗口 ActionBar 的 AppCompat 主题，Manifest 有 parentActivityName 或 PARENT_ACTIVITY meta-data，onOptionsItemSelected 处理 android.R.id.home；写错：页面规格的导航表写「ActionBar Up（若有）」，没写定 Up 箭头显不显示；或写「无返回箭头——源端未调 setDisplayHomeAsUpEnabled」而没提 parentActivityName
- rule-2bdecb39f1c1｜规格导航表里 Up 和系统返回各写一行，照源码各自的调用填｜读到：源码 android.R.id.home 分支调 super.onBackPressed() 或 finish()，onBackPressed 覆写里另有回退分支；写错：规格导航表把「ActionBar Up 尖角」和系统返回写成一行「与系统返回共用同一分支」，Up 也先走覆写里的回退

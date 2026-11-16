# 工具栏里的 SearchView 和 ActionBarDrawerToggle

agent 会看到什么：读到菜单 XML 的 item 用 SearchView 作 actionView（showAsAction 含 collapseActionView）、代码有 OnActionExpandListener、onQueryTextSubmit、supportInvalidateOptionsMenu，或 ActionBarDrawerToggle 的 setDrawerIndicatorEnabled、syncState；规格把它写成几个查询函数或「内化等价」，AC 没有展开收起、焦点、提交和菜单重建

## 规矩

- rule-70c1bddbe370｜源端工具栏行为由 SearchView、ActionBarDrawerToggle 承载时，规格按控件 API 列状态机｜读到：menu XML 的 item 用 SearchView 作 actionView、showAsAction 为 collapseActionView|always，代码里有 OnActionExpandListener、setOnQueryTextFocusChangeListener、onQueryTextSubmit、supportInvalidateOptionsMenu；或 ActionBarDrawerToggle 的 setDrawerIndicatorEnabled、syncState；写错：规格把 SearchView 写成几个查询函数，实现映射写「内化等价」「状态直调」；AC 里没有展开/收起、焦点、提交返回值与 ACTION_SEARCH 投递、菜单重建收起、空串不提交

# SAF 新建文档和 DocumentViewPicker 保存

agent 会看到什么：读到源端用 SAF 的 CreateDocument / ACTION_CREATE_DOCUMENT 按 MIME 让用户选导出位置；产物里 DocumentViewPicker.save 的 DocumentSaveOptions（newFileNames、fileSuffixChoices）

## 规矩

- rule-bb7605ac2a6f｜源端 CreateDocument 按 MIME 补后缀时，目标端 newFileNames 直接写带 .zip 的名字｜读到：源端用 SAF 的 CreateDocument（MIME 为 application/zip）launch("<不带后缀的名字>") 让用户选导出位置；写错：目标端 DocumentSaveOptions 的 newFileNames 照抄不带后缀的名字

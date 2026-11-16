# 复制到剪贴板（ClipboardManager）

agent 会看到什么：读到源端用 ClipboardManager.setPrimaryClip 放 ClipData（复制图片时放 FileProvider 生成的 URI）；产物里 pasteboard.createData 的 MIME 类型（MIMETYPE_TEXT_URI / MIMETYPE_PIXELMAP）、放进去的沙箱 URI 和复制成功后的提示

## 规矩

- rule-9244f827483d｜图片复制到剪贴板写 MIMETYPE_PIXELMAP 并补 Toast，不写沙箱 file URI｜读到：源端复制图片时用 FileProvider 生成的 URI 放进剪贴板（接收方凭跨应用授权读取）；写错：pasteboard.createData(pasteboard.MIMETYPE_TEXT_URI, 应用沙箱的 file:// URI)，成功后没有任何提示

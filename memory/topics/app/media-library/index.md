# app/media-library

系统媒体库直接读写：受限权限下的相机资产保存、最近媒体入口、删除确认与外部查看分享

[上一级](../index.md)

## 本级经验

- [deleteAssets 先授权再删，取消与失败分开](lesson-dd3bd947a05103e1f5f0.lesson.md) · 阶段：execute/repair · 信号：deleteAssets, MediaAssetChangeRequest.deleteAssets, WRITE_IMAGEVIDEO, ContentResolver.delete
- [最近媒体以自存 URI 为准，未授权不整库查询](lesson-43781ac1c21274acd48b.lesson.md) · 阶段：spec/execute · 信号：MediaStore, MediaStore.Images.Media.EXTERNAL_CONTENT_URI, getAssets, getThumbnail
- [查看分享媒体 URI 用精确 MIME 并授读权限](lesson-044358011be198c5bf87.lesson.md) · 阶段：spec/execute · 信号：ACTION_VIEW, ACTION_SEND, EXTRA_STREAM, startAbility
- [相机产出走系统资产保存，不靠受限写权限](lesson-bc279ce222e98e0d5ede.lesson.md) · 阶段：spec/execute · 信号：MediaStore, IS_PENDING, MediaRecorder, createAsset

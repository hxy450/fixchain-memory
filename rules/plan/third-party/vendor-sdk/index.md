# 计划里要平台 Key 的厂商 SDK

agent 会看到什么：规格或 skill 映射表里有高德等要平台 Key 的厂商 SDK（com.amap.api、PoiSearchV2），计划的步骤只挂了 hmos-sdk-docs 或连它都没有，scope 里没有 ohpm 依赖、初始化和 Key 注入

## 规矩

- rule-973f4d6dd2d6｜Slice 计划碰到厂商 SDK 时追加 hmos-sdk-docs，依赖声明和初始化列进 scope｜读到：skill 映射表把高德列为 hmos-sdk-docs 的厂商 SDK；feature spec 的范围写「高德地图、定位权限、POI 搜索」，数据流写「关键词→PoiSearchV2→结果列表」；写错：Slice 计划 Step 3c 的 suggested_skills 里没有 hmos-sdk-docs，scope 只列服务层、没有 SDK 依赖声明与初始化，占位表为空；或者把整套地图、定位、POI、路线能力登记为 deferred 占位
- rule-3ef0fda1ebf5｜计划里需要平台 Key 的厂商 SDK，显式排上依赖、初始化时机、Key 注入和缺 Key 验证项｜读到：源应用的地图、POI、导航依赖需要平台 Key 的厂商 SDK（如高德），规格的 API 候选为 AMap 定位/地图/POI/导航 SDK；写错：计划里该 SDK 的步骤只挂了一个 hmos-sdk-docs，没有 ohpm 依赖、隐私同意后初始化、Key 构建期注入，也没有 Key 缺失时的 needs_capture 运行期验证项

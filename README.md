# PsychonautWiki Journal (中文增强版)

基于 Jetpack Compose 开发的现代化离线个人用药记录与科学减害（Harm Reduction）参考工具。

[![Latest Release](https://img.shields.io/github/v/release/yuanyuan2233/psychonautwiki-journal-android-zh_CN?label=Release&color=blue)](https://github.com/yuanyuan2233/psychonautwiki-journal-android-zh_CN/releases/latest)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-green.svg)](LICENSE)
[![Android 8.0+](https://img.shields.io/badge/Android-8.0%2B-orange.svg)](https://developer.android.com/about/versions/oreo)
[![Offline & Private](https://img.shields.io/badge/Privacy-100%25%20Offline-success.svg)](https://github.com/yuanyuan2233/psychonautwiki-journal-android-zh_CN)

---

## 项目背景与维护声明

PsychonautWiki Journal 原由 Isaak Hanimann 开源维护（至 v11.11 版本）。本项目为该工具在开源社区的长期独立维护分支。

本项目遵循 GNU General Public License v3.0 协议持续维护，秉持以下原则：
- **完全开源**：代码与清洗工具全量公开透明；
- **离线与隐私优先**：应用不包含任何网络请求、遥测或数据分析代码，全部数据仅保留在用户设备本地；
- **科学与药理本土化**：结合临床药理学与国家药典规范，对物质数据与减害参考体系进行持续校准与扩充。

---

## v13.1 核心特性

### 1. 颜色体系扩充与 HSL 连续感知微调
- **13 种主色相与 117 档标准色阶**：ColorFamily 扩充至 13 类主色系并支持 100~900 完整标准色阶（共 117 种专业精选色），向下无缝兼容历史调色方案。
- **单轨明暗微调滑块**：在二级混色选取组件中引入基于 HSL 连续感知渐变的单轨明暗微调滑块，支持 1600 万真彩色自由定制。

### 2. 减害相互作用安全警报全链路修复
- **相互作用 100% 灵敏检出**：数据层恢复英文 Canonical 标引基底，在保持全中文本地化呈现的同时，彻底解决相互作用检查漏报与静默失效漏洞。
- **警告弹窗语言隔离**：优化 Compose 环境下字符串资源格式化生命周期，彻底根除警报弹窗中英混排与语言不跟随的问题。

### 3. 数据安全与健壮性加固
- **原子事务与导入安全守卫**：全量数据导入引入 Room `@Transaction` 单一原子事务，防止文件损坏导致原有数据库被清空；增加空文件与损坏防御。
- **时程与剂量阶梯校准**：修复阿扑吗啡（Apomorphine）吸食时程单位、25B-NBOH 剂量单位（µg）与跨月耐受度视图时间窗口过滤。
- **Release 构建安全规范**：应用包名后缀隔离（`.zh`），移除非必要明文备份风险，规范自动化签名与构建安全门禁。

---

## v13.0 历史特性

### 1. 药效时程叠加微积分引擎
- **多次给药连续叠加**：全库 517 个给药途径（ROA）完整补全起效、爬升、峰值、消退和总时长的五阶段时程参数，解决多次服药时时程曲线断裂的问题。
- **蓄积效应平滑拟合**：采用梯形微积分连续叠加算法，真实呈现多次服药在体内的血药浓度蓄积与二次达峰过程。

### 2. 耐受度时序分析（甘特矩阵）
- **耐受归零界线与倒计时**：甘特图动态绘制最长耐药周期的归零终点线与日期微标，并在追踪卡片中提供预计耐受归零倒计时。
- **双阶段耐受可视化**：校准经典致幻剂等物质的耐受衰减模型，支持完全耐受与半耐受双阶段渐变渲染。
- **客观数据标识**：对单次摄入不产生急性耐药的物质显式打上状态标签，并附带药理说明，保持数据严谨客观。

### 3. 应用内即时多语言系统
- **动态语言切换**：在设置中支持在「简体中文 / English / 跟随系统」之间实时热切换，无需重启应用。
- **物质名称双语联动**：中文模式优先匹配标准中文通用名，英文模式无缝还原国际非专利名称（WHO INN）。

### 4. 药典辞书规范化与全量汉化
- **用药安全机制汉化**：全量翻译数千条药物相互作用（DDI）机理、严重程度分级及用药禁忌警示。
- **物质通用名标准化**：参考《中华人民共和国药典》与国内外临床说明书，对物质名称进行学术消歧与同义词合并。

### 5. 底层颜色架构与数据库安全迁移
- **自由调色体系**：重构颜色存储架构为通用的 AppColor 模型，支持 HEX 色相与亮度自定义。
- **平滑兼容升级**：内置 Room 数据库自动化迁移（v7 至 v8），完全兼容老用户既有数据及历史备份的导入导出。

### 6. 全局无死锁手势导航
- 全面适配二级与三级页面的顶栏返回、系统物理返回键拦截及全面屏滑动手势，消除深层导航死锁。

---

## 功能全景

| 模块 | 主要功能 |
| :--- | :--- |
| **服药日记 (Journal)** | 快捷录入、ROA 给药途径选择、预设及自定义剂量、Shulgin 体验量表评级、事件笔记、药代微积分时程图。 |
| **药典检索 (Search)** | 收录 500+ 种精神活性物质与临床处方药；提供给药途径剂量阶梯、ADME 动力学参数与相互作用速查。 |
| **耐受分析 (Tolerance)** | 基于用户真实用药历史推演的甘特分析图、双阶段色带、归零界线与实时倒计时。 |
| **用药统计 (Stats)** | 物质伴侣频次图、用药日历、周/月/年多维度统计图表。 |
| **安全指南 (Guides)** | 化学试剂显色比对参考表、容积法稀释给药指南、给药途径生理防护说明。 |
| **设置与备份 (Settings)** | 100% 离线运行、JSON 全量明文导入导出、应用内语言切换、物质色彩深度定制。 |

---

## 下载与安装

从 [GitHub Releases 页面](https://github.com/yuanyuan2233/psychonautwiki-journal-android-zh_CN/releases/latest) 下载预编译的稳定版 APK：

- **系统要求**：Android 8.0 (API 26) 及以上
- **包名说明**：采用独立包名（`com.isaakhanimann.journal.zh`），支持与原版 Journal 共存安装。

---

## 本地编译

### 环境要求
- JDK 17
- Android SDK 35
- Gradle 8.11.1+

### 编译步骤
```bash
git clone https://github.com/yuanyuan2233/psychonautwiki-journal-android-zh_CN.git
cd psychonautwiki-journal-android-zh_CN

# 生产环境 Release APK 构建（启用 R8 混淆、资源压缩与独立包名）
./gradlew assembleRelease

# 或本地调试构建（仅供开发测试）
./gradlew assembleDebug
```
产物位置：`app/build/outputs/apk/release/app-release-unsigned.apk`（或配置签名后生成的 release APK）以及 `app/build/outputs/apk/debug/app-debug.apk`。

---

## 致谢与数据来源

本项目的数据整理、药理模型与汉化资料受益于以下开源项目与知识库：

- **Isaak Hanimann**：原版 PsychonautWiki Journal 的架构设计与核心代码作者；
- **PsychonautWiki**：全球同行评议物质药理学数据与开放 API；
- **FreeODwiki 社群**：中文物质学名考证、命名规范化及中文减害资料；
- **TripSit**：开源物质数据库与多物质相互作用对照表（TripSit/drugs）；
- **国家药典委员会与国家卫生健康委**：《中华人民共和国药典》、《国家基本药物目录》药品通用名称规范。

---

## 减害与免责声明

1. 本应用旨在倡导风险减害（Harm Reduction）理念，所载药理参数、剂量区间及相互作用数据均整理自公开学术文献与同行评议研究，仅供科学参考与个人健康记录，不作为临床医疗诊断或处方凭证。
2. 本项目坚决反对任何形式的违法涉药或滥用行为。
3. 遇有急性药物反应或医疗意外，请立即拨打当地急救电话寻求专业医疗救助。

---

## 许可证

本项目依据 [GNU General Public License v3.0](LICENSE) 持续开源：
- 原版版权所有 (C) 2022–2024 Isaak Hanimann.
- 中文版维护 (C) 2026 yuanyuan2233 与开源贡献者.

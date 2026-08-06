# 🪷 莲之空棉花娃娃收集进度

ラブライブ！蓮ノ空女学院スクールアイドルクラブ ぬいぐるみ コレクションチェッカー

> LoveLive! 莲之空女学院学园偶像俱乐部 棉花娃娃（ぬいぐるみ）收集进度记录工具。

在线访问：<https://fhlm.github.io/hasunosora-nui-checker/>

## 功能

- 📋 列表展示官网收录的 48 款棉花娃娃商品（按系列 · 款式 · 发售批次组织）
- 💗 勾选已收集角色（区分通常版 / 限定版，同系列同版本联动）
- 🔍 搜索（系列 / 商品 / 角色）、按发售时间排序、角色筛选
- 🖼️ 点击封面图放大查看
- 🌐 中日文界面切换
- 📱 手机端 H5 适配
- 💾 进度保存在本地浏览器（localStorage）

## 数据来源

[Love Live! 莲之空女学院 公式官网 GOODS](https://www.lovelive-anime.jp/hasunosora/goods/)（截至 2026-08-06）

本页面为非官方粉丝工具 · 仅供个人学习参考 · 商品信息以官网为准 · 版权归各权利方所有

## 构建

```bash
# 修改 build.py 数据 / template.html 模板后重建
python build.py
```

- `index.html`：构建产物（数据内嵌，无外部依赖）
- `template.html`：页面模板（含 `__DATA__` 占位符）
- `thumbs/`：商品缩略图（webp）

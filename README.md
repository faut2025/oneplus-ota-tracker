# OnePlus OTA Tracker

OPPO/OnePlus 机型 OTA 动态数据源

## 概述

本仓库通过 GitHub Actions 自动追踪和更新 OPPO/OnePlus 机型的 OTA（Over-The-Air）系统更新信息。

## 数据更新

数据每周一北京时间 17:00 自动更新，也可手动触发更新。

## 数据来源

- **实时数据**: [ota-tracker.linesoft.top](https://ota-tracker.linesoft.top)
- **历史归档**: daxiaamu/yun.daxiaamu.com

## 目录结构

```
.
├── .github/
│   └── workflows/
│       └── update-ota.yml    # 自动更新工作流
├── data/
│   └── ota_info.json         # OTA 数据文件
└── README.md
```

## GitHub Pages

更新后的数据会发布到 GitHub Pages：
https://faut2025.github.io/oneplus-ota-tracker/

## 支持的机型

### OnePlus
- OnePlus 15 系列 (PLK110, PLZ110)
- OnePlus 13 系列 (PJZ110, PKX110)
- OnePlus 12 (PJD110)
- OnePlus 11 (PHB110)
- OnePlus Ace 系列
- OnePlus 平板系列

### OPPO
- Find 系列
- Reno 系列
- Pad 系列

## License

MIT

# tvbox-selfhost

自托管 TVBox 配置文件，不依赖任何外部上游服务。基于饭太硬配置结构，完全去除品牌化引用，所有资源本地化。

## 订阅地址

```bash
# 主配置（推荐）
https://cdn.jsdelivr.net/gh/Trysknee01/tvbox-selfhost@main/config.json

# 备用
https://raw.githubusercontent.com/Trysknee01/tvbox-selfhost/main/config.json
```

## 包含内容

| 目录/文件 | 说明 |
|-----------|------|
| `config.json` | 主配置文件（去品牌化） |
| `FTY/` | drpy2 爬虫 JS |
| `jar/` | java spider + fan.txt |
| `lib/` | 库文件 + 直播 m3u + txt 资源 |
| `js/` | 直播 JS + 数据源 |
| `json/` | 云盘/教育/分类配置 |
| `py/` | Python 工具 |
| `tools/` | 构建脚本 |
| `tvfan/` | Cloud-drive 模板 |

## 与原版区别

- 所有 `nos.netease.com` / `file.icve.com.cn` 资源 → `lib/` 本地
- 饭太硬壁纸/logo → 移除
- `js/live2mv_data.json` / `js/lf_live.txt` → 去除饭太硬条目
- `lib/live2cms.js` → 本地直播源
- `tvfan/Cloud-drive.txt` → 本地云盘模板

## 自行维护

1. Fork 本仓库
2. 修改 `config.json` 中的 sites 列表
3. GitHub Actions 自动同步直播源（可选）

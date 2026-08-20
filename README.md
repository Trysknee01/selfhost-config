# selfhost-config

自托管 TVBox 配置文件，不依赖任何外部上游服务。

## 订阅地址

```bash
# 主配置（推荐）
https://cdn.jsdelivr.net/gh/Trysknee01/selfhost-config@main/config.json

# 备用
https://raw.githubusercontent.com/Trysknee01/selfhost-config/main/config.json
```

GitHub Pages（Pages 已启用）：

```
https://trysknee01.github.io/selfhost-config/config.json
```

## 自动同步

每天北京时间 10:00 自动从上游抓取最新配置，去品牌化并本地化后自动推送。

手动触发：GitHub → Actions → "Auto Sync Config" → Run workflow

## 包含内容

| 目录 | 说明 |
|------|------|
| `config.json` | 主配置文件 |
| `FTY/` | drpy2 爬虫 JS |
| `jar/` | spider jar + fan.txt |
| `lib/` | 库文件 + 直播资源 |
| `js/` | 直播 JS + 数据源 |
| `json/` | 云盘/教育/分类 |
| `py/` | Python 工具 |
| `tools/` | 构建脚本 |
| `tvfan/` | Cloud-drive |

## 自行维护

1. Fork 仓库
2. 修改 `config.json` 中 sites
3. push 即可

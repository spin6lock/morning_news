# 早安新闻助手

一个每日自动获取新闻、诗句和天气的命令行工具，支持定时推送。

## 功能特性

- 📰 **每日新闻**: 获取当日精选新闻资讯
- 📜 **励志诗句**: 推送古诗词名句
- 🔥 **网络热点**: 使用 Claude AI 搜索网络热点新闻，按领域分类
- 🌤️ **天气预报**: 提供3天天气预报
- 🤖 **自动推送**: 支持定时自动推送（需配置cron任务）
- 📝 **Markdown输出**: 格式化输出，易于阅读和分享

## 安装依赖

```bash
pip3 install requests
```

## 配置说明

### 1. 复制配置模板

```bash
cp config_example.py config.py
```

### 2. 编辑配置文件

修改 `config.py` 文件，填入你的API配置：

```python
# 和风天气API配置
weather_api_key = "YOUR_WEATHER_API_KEY"  # 请填写你的和风天气API key
weather_host = "YOUR_WEATHER_HOST"        # 请填写你的和风天气API host

# 新闻API配置（60秒看世界）
news_api_url = "http://localhost:4399/v2/60s"  # 无需token认证的新闻API地址

# 诗句API Token（今日诗词）
poem_api_token = "YOUR_POEM_API_TOKEN"  # 请填写你的今日诗词token，留空则跳过诗句获取
```

### API申请说明

- **和风天气**: 访问 [https://dev.qweather.com](https://dev.qweather.com) 注册申请
- **今日诗词**: 访问 [https://www.jinrishici.com](https://www.jinrishici.com) 申请token
- **新闻API**: 60秒看世界API地址，无需申请token

## 使用方法

### 基础命令

```bash
# 获取所有信息（诗句、热点新闻、新闻、天气）
python3 main.py --all

# 仅获取新闻
python3 main.py --news

# 仅获取诗句
python3 main.py --poem

# 仅获取热点新闻
python3 main.py --hotnews

# 仅获取天气
python3 main.py --weather

# 输出模式（仅输出markdown结果，无调试信息）
python3 main.py --all -o
```

### 参数说明

- `--all`: 获取所有信息（诗句、热点新闻、新闻、天气）
- `--news`: 仅获取新闻
- `--poem`: 仅获取诗句
- `--hotnews`: 仅获取热点新闻
- `--weather`: 仅获取天气
- `-o` / `--output`: 输出模式，仅输出markdown内容

### 输出示例

```markdown
# 📜 每日诗句

**诗句内容**

---

**唐代·作者《作品名》**

诗词正文...

# 🔥 网络热点新闻

## 科技
1. 科技新闻1
2. 科技新闻2
...

## 财经
1. 财经新闻1
...

## 国际
...

## 社会
...

## 娱乐
...

# 📰 每日新闻

**日期:** 2025-11-20 (星期四) 乙巳年十月初二

来源: 获取成功，开源地址 https://github.com/vikiboss/60s

---

1. 新闻标题1
2. 新闻标题2
...

# 📜 每日诗句

**诗句内容**

---

**唐代·作者《作品名》**

诗词正文...

# 🌤️ 天气预报

**更新时间:** 2025-11-21T00:02+08:00

## 今天 (2025-11-21)

**多云 晴**
🌡️ 温度: **11°C** ~ **20°C**
...
```

## 定时推送

### 使用daily_run.sh

项目提供了 `daily_run.sh` 脚本，可用于每日自动推送：

```bash
chmod +x daily_run.sh
```

### 配置cron任务

每天早上7:58自动推送（提前2分钟执行）：

```bash
# 编辑crontab
crontab -e

# 添加以下行
58 7 * * * /home/spin6lock/opensource/morning_news/daily_run.sh
```

### 手动运行

```bash
./daily_run.sh
```

## 文件说明

- `main.py`: 主程序文件
- `config.py`: 配置文件（需自行创建）
- `config_example.py`: 配置模板文件
- `daily_run.sh`: 每日自动推送脚本
- `today.md`: 每日推送内容输出文件

## 错误排查

### 新闻获取失败

- 检查 `news_api_url` 是否正确
- 确认本地新闻API服务是否正常运行
- 检查网络连接

### 诗句获取失败

- 检查 `poem_api_token` 是否正确配置
- 确认token未过期

### 天气获取失败

- 检查 `weather_api_key` 和 `weather_host` 是否正确
- 确认和风天气API账户状态

## 许可证

本项目仅供学习和研究使用。

## 致谢

- 感谢 [60秒看世界](https://github.com/vikiboss/60s) 提供新闻数据
- 感谢 [今日诗词](https://www.jinrishici.com) 提供诗词API
- 感谢 [和风天气](https://www.qweather.com) 提供天气API

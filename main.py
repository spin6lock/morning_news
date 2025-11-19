import requests
import argparse
from config import weather_api_key, weather_host, news_api_token, poem_api_token

def get_news():
    """获取每日新闻"""
    print("正在获取新闻...")
    if not news_api_token:
        print("跳过新闻获取：未配置news_api_token")
        return {"skipped": True, "message": "未配置新闻API Token"}
    try:
        news_url = "https://v2.alapi.cn/api/zaobao"
        params = {"token": news_api_token}
        news_response = requests.get(news_url, params=params)
        news_response.raise_for_status()  # 检查HTTP错误
        news = news_response.json()
        print("新闻获取完成")
        return news
    except requests.exceptions.RequestException as e:
        print(f"获取新闻失败: {e}")
        return {"error": str(e)}

def get_poem():
    """获取励志诗句"""
    print("正在获取诗句...")
    if not poem_api_token:
        print("跳过诗句获取：未配置poem_api_token")
        return {"skipped": True, "message": "未配置诗句API Token"}
    try:
        poem_url = "https://v2.jinrishici.com/sentence"
        headers = {"X-User-Token": poem_api_token}
        poem_response = requests.get(poem_url, headers=headers)
        poem_response.raise_for_status()
        poem = poem_response.json()

        # 检查返回状态
        if poem.get('status') != 'success':
            print(f"诗句API返回错误: {poem.get('status')}")
            return {"error": f"API错误: {poem.get('status')}"}

        # 转换为markdown格式
        poem_md = "# 📜 每日诗句\n\n"

        data = poem.get('data', {})
        origin = data.get('origin', {})

        # 获取推荐内容并加粗显示
        recommended = data.get('content', '')
        if recommended:
            poem_md += f"**{recommended}**\n\n"

        # 获取原始诗句
        content = origin.get('content', [])
        if content:
            poem_md += "---\n\n"
            poem_md += f"**{origin.get('dynasty', '')}·{origin.get('author', '')}《{origin.get('title', '')}》**\n\n"
            for line in content:
                poem_md += f"{line}\n\n"

        print("诗句获取完成")
        return poem_md

    except requests.exceptions.RequestException as e:
        print(f"获取诗句失败: {e}")
        return {"error": str(e)}

def get_weather():
    """获取当天天气"""
    print("正在获取天气...")
    try:
        # 使用config中的weather_host
        weather_url = f"https://{weather_host}/v7/weather/3d"
        weather_params = {
            "location": "101280108",  # 城市ID 广州市海珠区
            "lang": "zh",
            "unit": "m",
            "key": weather_api_key  # 添加API密钥
        }
        weather_response = requests.get(weather_url, params=weather_params)
        weather_response.raise_for_status()
        weather = weather_response.json()

        # 检查返回状态
        if weather.get('code') != '200':
            print(f"天气API返回错误: {weather.get('code')}")
            return {"error": f"API错误: {weather.get('code')}"}

        # 转换为markdown格式
        weather_md = "# 🌤️ 天气预报\n\n"
        weather_md += f"**更新时间:** {weather.get('updateTime', 'N/A')}\n\n"

        daily = weather.get('daily', [])
        for i, day in enumerate(daily):
            date = day.get('fxDate', '')
            # 格式化日期
            if i == 0:
                date_str = f"今天 ({date})"
            elif i == 1:
                date_str = f"明天 ({date})"
            else:
                date_str = f"后天 ({date})"

            weather_md += f"## {date_str}\n\n"
            weather_md += f"**{day.get('textDay', '')} {day.get('textNight', '')}**  \n"
            weather_md += f"🌡️ 温度: **{day.get('tempMin', '')}°C** ~ **{day.get('tempMax', '')}°C**  \n"
            weather_md += f"☀️ 日出: {day.get('sunrise', '')} | 🌙 日落: {day.get('sunset', '')}  \n"
            weather_md += f"🌬️ 风向: {day.get('windDirDay', '')} {day.get('windScaleDay', '')}级  \n"
            weather_md += f"💧 湿度: {day.get('humidity', '')}% | 🌧️ 降水: {day.get('precip', '')}mm  \n"
            weather_md += f"👁️ 能见度: {day.get('vis', '')}km | ☀️ 紫外线: {day.get('uvIndex', '')}  \n"
            weather_md += f"🌙 月相: {day.get('moonPhase', '')}  \n\n"

        print("天气获取完成")
        return weather_md

    except requests.exceptions.RequestException as e:
        print(f"获取天气失败: {e}")
        return {"error": str(e)}

def main():
    parser = argparse.ArgumentParser(description='早安新闻助手 - 可控制获取的新闻、诗句和天气')
    parser.add_argument('--news', action='store_true', help='获取新闻')
    parser.add_argument('--poem', action='store_true', help='获取诗句')
    parser.add_argument('--weather', action='store_true', help='获取天气')
    parser.add_argument('--all', action='store_true', help='获取所有信息（默认）')

    args = parser.parse_args()

    # 如果没有指定任何参数，默认获取所有信息
    if not any([args.news, args.poem, args.weather, args.all]):
        args.all = True

    result = {}
    markdown_output = []  # 收集markdown格式的输出

    if args.all or args.news:
        news_result = get_news()
        if isinstance(news_result, str) and news_result.startswith('#'):
            markdown_output.append(news_result)
        else:
            result["news"] = news_result

    if args.all or args.poem:
        poem_result = get_poem()
        if isinstance(poem_result, str) and poem_result.startswith('#'):
            markdown_output.append(poem_result)
        else:
            result["poem"] = poem_result

    if args.all or args.weather:
        weather_result = get_weather()
        if isinstance(weather_result, str) and weather_result.startswith('#'):
            markdown_output.append(weather_result)
        else:
            result["weather"] = weather_result

    # 输出结果
    print("\n" + "="*50)
    print("获取结果:")
    print("="*50)

    # 先输出markdown格式的内容
    for md in markdown_output:
        print(md)
        print()

    # 再输出JSON格式的内容
    if result:
        print(result)

if __name__ == "__main__":
    main()

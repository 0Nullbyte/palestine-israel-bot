import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

async def liveaumap():
    url = "https://israelpalestine.liveuamap.com/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        scroll_container = soup.find('div', id='feedler')
        events = scroll_container.find_all('div', class_='event')

        news_items = []
        for event in events:
            title = event.find('div', class_='title').text.strip()
            link = event.find('a', class_='comment-link')['href']
            news_items.append({'title': title, 'link': link})

        return news_items[:5]  
    return None

async def fetchnews():
    url_aljazeera = "https://www.aljazeera.com/news/"
    url_youtube = "https://www.youtube.com/@aljazeera/streams"

    response_aljazeera = requests.get(url_aljazeera)
    response_youtube = requests.get(url_youtube)

    ITEMS = []

    if response_aljazeera.status_code == 200:
        soup = BeautifulSoup(response_aljazeera.text, 'html.parser')
        articles = soup.find_all('a', class_='topic-title')

        for article in articles:
            title = article.text.strip()
            link = article['href']
            ITEMS.append({'title': f"[{title}]({link})", 'link': link})

    if response_youtube.status_code == 200:
        soup = BeautifulSoup(response_youtube.text, 'html.parser')
        streams = soup.find_all('a', class_='style-scope ytd-grid-video-renderer')

        for stream in streams:
            title = stream.find('div', class_='style-scope ytd-grid-video-renderer').text.strip()
            link = "https://www.youtube.com" + stream['href']
            alternative_items.append({'title': f"[{title}]({link})", 'link': link})

    return ITEMS[:5] 

@bot.event
async def on_ready():
    print(f'{bot.user} has connected successfully.')

@bot.command(name='news')
async def news(ctx):
    liveaumap = await liveaumap()
    fetchnews = await fetchnews()

    if liveuamap_news:
        embed = discord.Embed(
            title="📰 Latest News 📰",
            color=0x7289da
        )

        for i, item in enumerate(liveuamap_news):
            embed.add_field(name=f"News {i+1}", value=f"[{item['title']}]({item['link']})", inline=False)

        footer = ""
        for i, item in enumerate(alternative_news):
            stream_text += f"{i+1}. {item['title']}\n{item['link']}\n"

        footer += f"🔥 Al Jazeera Stream 🔥 (https://www.youtube.com/watch?v=bNyUyrR0PHo)  [Watch here]\n"
        footer += f"🔥 Al Jazeera News 🔥 (https://www.aljazeera.com/news/)  [Read here]\n"
        footer += "Crafted by Ayham 💗\n\n"

        embed.set_footer(text=f"Streams:\n{stream_text}")
        embed.set_image(url="https://israelpalestine.liveuamap.com/images/shr/002.png")

        await ctx.send(embed=embed)
        print("News and streams sent successfully.")
    else:
        await ctx.send("Unable to retrieve news from liveuamap. Please try again later.")
        print("News retrieval failed.")

bot.run('YOUR_BOT_TOKEN')

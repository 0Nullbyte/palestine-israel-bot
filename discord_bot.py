
import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests

#Made By Ayhxm

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

async def scrape_liveuamap():
    url = "https://israelpalestine.liveuamap.com/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        scroll_container = soup.find('div', id='feedler')
        events = scroll_container.find_all('div', class_='event')

        news_list = []
        for event in events:
            title = event.find('div', class_='title').text.strip()
            link = event.find('a', class_='comment-link')['href']
            news_list.append({'title': title, 'link': link})

        return news_list[:5]  
    else:
        return None

async def scrape_alternative_news():

    alternative_news_source_aljazeera = "https://www.aljazeera.com/news/"
    response_aljazeera = requests.get(alternative_news_source_aljazeera)
    

    alternative_news_source_youtube = "https://www.youtube.com/@aljazeera/streams"
    response_youtube = requests.get(alternative_news_source_youtube)

    alternative_news_list = []

    if response_aljazeera.status_code == 200:
        soup_aljazeera = BeautifulSoup(response_aljazeera.text, 'html.parser')
        articles_aljazeera = soup_aljazeera.find_all('a', class_='topic-title')

        for article in articles_aljazeera:
            title = article.text.strip()
            link = article['href']
            alternative_news_list.append({'title': f"[{title}]({link})", 'link': link})


    if response_youtube.status_code == 200:
        soup_youtube = BeautifulSoup(response_youtube.text, 'html.parser')
        streams_youtube = soup_youtube.find_all('a', class_='style-scope ytd-grid-video-renderer')

        for stream in streams_youtube:
            title = stream.find('div', class_='style-scope ytd-grid-video-renderer').text.strip()
            link = "https://www.youtube.com" + stream['href']
            alternative_news_list.append({'title': f"[{title}]({link})", 'link': link})

    return alternative_news_list[:5] 

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(name='news')
async def news(ctx):
    liveuamap_news = await scrape_liveuamap()
    alternative_news = await scrape_alternative_news()

    if liveuamap_news:
        embed = discord.Embed(
            title="📰Latest News📰",
            color=0x7289da  
        )

        for i, article in enumerate(liveuamap_news):
            embed.add_field(name=f"News {i+1}", value=f"[{article['title']}]({article['link']})", inline=False)


        streams_text = ""
        for i, article in enumerate(alternative_news):
            streams_text += f"{i+1}. {article['title']}\n{article['link']}\n"


        streams_text += f"🔥Al Jazeera Stream🔥 (https://www.youtube.com/watch?v=bNyUyrR0PHo)  [Watch here]\n"
        streams_text += f"🔥Al Jazeera News🔥 (https://www.aljazeera.com/news/)  [Read here]\n"
        streams_text += f"Made By Ayham💗\n\n"


        embed.set_footer(text=f"Streams:\n{streams_text}")


        image_url = "https://israelpalestine.liveuamap.com/images/shr/002.png"  
        embed.set_image(url=image_url)

        await ctx.send(embed=embed)
        print("Sent news, streams, and image.")
    else:
        await ctx.send("Error fetching news from liveuamap. Please try again later.")
        print("Failed to fetch news")


bot.run('YOUR_BOT_TOKEN')

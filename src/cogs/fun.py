import random
import disnake
import disnake_paginator

from disnake.ext import commands
from exts import EIGHTBALL_ANSWERS, COMPLIMENTS
from kurisu import Kurisu, KurisuContext


class Fun(
    commands.Cog, command_attrs={"cooldown": commands.CooldownMapping.from_cooldown(1, 2.5, commands.BucketType.user)}
):
    """Some fun stuff"""

    def __init__(self, bot: Kurisu):
        self.bot = bot

    async def get_ud_results(self, term: str, max: int = 5):
        async with self.bot.session as session:
            async with session.get(f"https://api.urbandictionary.com/v0/define?term={term}") as resp:
                try:
                    return (await resp.json())["list"][:max]
                except (IndexError, KeyError):
                    pass
        await session.close()

    @commands.command(name="8ball", aliases=["8b", "eightball"])
    async def _8ball(self, ctx: KurisuContext, *, question: str):
        """Ask a question and let the mystical 8ball answer for you!"""
        await ctx.send(
            embed=disnake.Embed(
                title="🎱The Mystical 8ball🎱",
                description=f"Question: {question}\nAnswer: {random.choice(EIGHTBALL_ANSWERS)}",
                color=self.bot.info_color,
            ).set_footer(text=f"Asked by {ctx.author}")
        )

    @commands.command()
    async def compliment(self, ctx: KurisuContext, *, member: disnake.Member = None):
        """Compliment yourself or someone else"""
        member = member or ctx.author
        await ctx.send(
            embed=disnake.Embed(
                description=f"{member.mention} {random.choice(COMPLIMENTS)}", color=self.bot.info_color
            ).set_footer(text=f"Compliment from {ctx.author}")
        )

    @commands.command(aliases=["owo"])
    async def owoify(self, ctx: KurisuContext, *, text: str):
        """Owoify text"""
        if len(text) > 200:
            return await ctx.send_error("Text is not allowed to be over 200 characters")
        async with self.bot.session.get(f"https://nekos.life/api/v2/owoify?text={text}") as resp:
            if resp.status == 200:
                await ctx.send_info((await resp.json())["owo"])
            else:
                await ctx.send_error(f"API returned a {resp.status} instead of a 200")

    @commands.command(aliases=["aq"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def animequote(self, ctx: KurisuContext):
        """Recieve an anime quote from the AnimeChan API"""
        async with self.bot.session.get("https://animechan.vercel.app/api/random") as resp:
            if resp.status == 200:
                quote = (await resp.json())["quote"]
                char = (await resp.json())["character"]
                anime = (await resp.json())["anime"]
                await ctx.send(
                    embed=disnake.Embed(description=f"{quote}\n~{char}", color=self.bot.info_color).set_footer(
                        text=f"Anime: {anime}"
                    )
                )
            else:
                await ctx.send(
                    embed=disnake.Embed(
                        description=f"API threw a {resp.status}. Please try again later.", color=self.bot.error_color
                    )
                )

    @commands.command(aliases=["urbandict"])
    @commands.cooldown(1, 4.5, commands.BucketType.user)
    async def ud(self, ctx: KurisuContext, *, term: str):
        """Query the Urban Dictionary API with a term"""
        results = await self.get_ud_results(term)
        embeds: list[disnake.Embed] = []

        for i in results:
            embeds.append(
                disnake.Embed(
                    title=f"Definition for {term}",
                    description=f"Definition: {i['definition']}",
                    color=self.bot.ok_color,
                )
                .set_footer(text=f"👍: {i['thumbs_up']}")
                .add_field(name="Author", value=i["author"] or "No Author ")
            )

        await disnake_paginator.ButtonPaginator(segments=embeds).start(ctx)

    @commands.command()
    async def maid(self, ctx: KurisuContext):
        """Maids go brrr"""
        async with self.bot.session.get("https://api.waifu.im/sfw/maid") as resp:
            await ctx.send(
                embed=disnake.Embed(color=self.bot.info_color).set_image(url=(await resp.json())["images"][0]["url"])
            )

    @commands.command()
    async def waifu(self, ctx: KurisuContext):
        """Waifu go brrr"""
        async with self.bot.session.get("https://api.waifu.im/sfw/waifu") as resp:
            await ctx.send(
                embed=disnake.Embed(color=self.bot.info_color).set_image(url=(await resp.json())["images"][0]["url"])
            )


def setup(bot: Kurisu):
    bot.add_cog(Fun(bot))

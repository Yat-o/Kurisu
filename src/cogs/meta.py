import os

from discord.ext import commands
import discord
import psutil

from core import Asahi, AsahiContext, PrefixHandler


class Meta(
    commands.Cog, command_attrs={"cooldown": commands.CooldownMapping.from_cooldown(1, 3.5, commands.BucketType.user)}
):
    """Base commands"""

    def __init__(self, bot: Asahi):
        self.bot = bot
        self.prefix_handler = PrefixHandler(self.bot)

    @commands.command()
    async def ping(self, ctx: AsahiContext):
        """Obligitory ping command"""
        msg = await ctx.send("Measuring now...")
        await msg.edit(
            content=None,
            embed=discord.Embed(description=f"Ping for {self.bot.user}", color=self.bot.info_color)
            .add_field(name="WebSocket Latency", value=f"{round(self.bot.latency * 1000)}ms")
            .add_field(
                name="Message", value=f"{round((msg.created_at - ctx.message.created_at).total_seconds() * 1000)}ms"
            ),
        )

    @commands.command()
    async def prefix(self, ctx: AsahiContext, *, prefix: str = None):
        """Set a guilds custom prefix. If none provided the set one will be provided"""
        if not prefix:
            return await ctx.send_info(f"This guild's prefix is `{self.bot.get_custom_prefix(ctx.guild.id)}`")
        if ctx.author.guild_permissions.manage_guild:
            self.prefix_handler.add_prefix(prefix[:10], ctx.guild.id)
            await ctx.send_ok("Prefix set!")
        else:
            await ctx.send_error("You are lacking the required permission to run this command: `Manage Server`")

    @commands.command()
    async def credits(self, ctx: AsahiContext):
        """Yes..."""
        await ctx.send(
            embed=discord.Embed(
                title="Credits",
                description=(
                    "Author: [Yat-o](https://github.com/Yat-o)\n"
                    "Contributors: A Full list can be found [here](https://github.com/Yat-o/Asahi/graphs/contributors)\n"
                    f"Registered Bot Owners: {', '.join([str(await self.bot.fetch_user(o)) for o in self.bot.owner_ids])}\n"
                    "Source Code: Can be found [here](https://github.com/Yat-o/Asahi/) "
                ),
            ).set_thumbnail(url=self.bot.user.avatar.url)
        )

    @commands.command()
    async def invite(self, ctx: AsahiContext):
        """Dms you with an invite link to invite the bot with"""
        await ctx.send_info(
            f"Invite me using [this link](https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&permissions=413893192823&scope=bot)"
        )


async def setup(bot: Asahi):
    await bot.add_cog(Meta(bot))

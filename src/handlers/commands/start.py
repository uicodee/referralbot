from aiogram import Router, types
from aiogram.filters import CommandStart, CommandObject

from src.infrastructure.database.dao import HolderDao

router = Router()


@router.message(CommandStart())
async def on_cmd_start(message: types.Message, dao: HolderDao, command: CommandObject):
    user = await dao.user.get_user_by_telegram_id(
        telegram_id=message.from_user.id
    )
    if user is None:
        user = await dao.user.add_user(
            telegram_id=message.from_user.id,
            full_name=message.from_user.full_name,
            username=message.from_user.username
        )
        if command.args is not None:
            await dao.user.update_balance(
                balance=user.balance + 1000,
                telegram_id=int(command.args)
            )
            await message.bot.send_message(
                chat_id=int(command.args),
                text="Siz yangi odam qoshdingiz!"
            )
    bot = await message.bot.get_me()
    link = f"https://t.me/{bot.username}?start={message.from_user.id}"
    await message.answer(
        text=f"Hello, {message.from_user.full_name}!\n"
             f"{link}\n"
             f"Balans: {int(user.balance)}",
        disable_web_page_preview=True
    )


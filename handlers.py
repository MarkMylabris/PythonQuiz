from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from quiz_data import quiz_data
from database import get_quiz_index, update_quiz_index, get_user_score, get_user_answers, get_statistics

router = Router()


def generate_options_keyboard(answer_options, right_answer):
    builder = InlineKeyboardBuilder()
    for option in answer_options:
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data="right_answer" if option == right_answer else "wrong_answer")
        )
    builder.adjust(1)
    return builder.as_markup()


@router.callback_query(F.data == "right_answer")
async def right_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    user_id = callback.from_user.id
    current_question_index = await get_quiz_index(user_id)
    user_answer = quiz_data[current_question_index]['options'][quiz_data[current_question_index]['correct_option']]

    await callback.message.answer(f"Ваш ответ: {user_answer}\nВерно!")

    current_score = await get_user_score(user_id) + 1
    current_question_index += 1
    await update_quiz_index(user_id, current_question_index, current_score, user_answer)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, user_id)
    else:
        await callback.message.answer(f"Квиз завершен! Ваш результат: {current_score}/{len(quiz_data)}")


@router.callback_query(F.data == "wrong_answer")
async def wrong_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    user_id = callback.from_user.id
    current_question_index = await get_quiz_index(user_id)
    correct_option = quiz_data[current_question_index]['correct_option']
    user_answer = callback.data  # This will need to be mapped to actual answer text

    # Find which option was selected
    for i, option in enumerate(quiz_data[current_question_index]['options']):
        if callback.data == "wrong_answer" and option != quiz_data[current_question_index]['options'][correct_option]:
            user_answer = option
            break

    await callback.message.answer(
        f"Ваш ответ: {user_answer}\nНеправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")

    current_score = await get_user_score(user_id)
    current_question_index += 1
    await update_quiz_index(user_id, current_question_index, current_score, user_answer)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, user_id)
    else:
        await callback.message.answer(f"Квиз завершен! Ваш результат: {current_score}/{len(quiz_data)}")


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    builder.add(types.KeyboardButton(text="Статистика"))
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))


async def get_question(message, user_id):
    current_question_index = await get_quiz_index(user_id)
    correct_index = quiz_data[current_question_index]['correct_option']
    opts = quiz_data[current_question_index]['options']
    kb = generate_options_keyboard(opts, opts[correct_index])
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)


async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 0
    await update_quiz_index(user_id, current_question_index, score=0, answer="")
    await get_question(message, user_id)


@router.message(F.text == "Начать игру")
@router.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    await message.answer("Давайте начнем квиз!")
    await new_quiz(message)


@router.message(F.text == "Статистика")
@router.message(Command("stats"))
async def cmd_stats(message: types.Message):
    stats = await get_statistics()
    if not stats:
        await message.answer("Статистика пока пуста!")
        return

    response = "Статистика игроков:\n"
    for user_id, score in stats:
        response += f"Пользователь {user_id}: {score}/{len(quiz_data)}\n"
    await message.answer(response)
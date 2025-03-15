async def get_balance(user_id: int, redis):
    balance = await redis.get(user_id)
    return balance if balance else 0


async def update_balance(user_id: int, amount: float, is_expense: bool, redis):
    balance = await redis.get(user_id)
    if not balance:
        balance = 0
    if is_expense:
        await redis.set(user_id, float(balance) - amount)
    await redis.set(user_id, float(balance) + amount)

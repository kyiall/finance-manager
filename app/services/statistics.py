import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings

from app.models.transactions import Transaction


class StatisticsService:
    @staticmethod
    async def update_statistics(db: AsyncSession, user_id: int, transaction: Transaction, add: bool):
        from app.crud.transactions import get_grouped_transactions
        incomes, expenses = await get_grouped_transactions(db, user_id)
        expense_dates = {expense.created_at.date() for expense in expenses}
        income_dates = {income.created_at.date() for income in incomes}
        total_expense = sum(expense.amount for expense in expenses)
        total_income = sum(income.amount for income in incomes)
        average_expense = total_expense / len(expense_dates) if len(expense_dates) > 0 else 0
        average_income = total_income / len(income_dates) if len(income_dates) > 0 else 0
        date = transaction.created_at.date()
        is_expense = transaction.is_expense
        amount = transaction.amount
        data = {
            "user_id": user_id,
            "average_income": round(average_income, 2),
            "average_expense": round(average_expense, 2),
            "date": date.isoformat(),
            "amount": amount,
            "add": add,
            "is_expense": is_expense
        }
        url = settings.STATS_SERVICE_URL
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data)
            print(response.text)

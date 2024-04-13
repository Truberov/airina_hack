import httpx

from balance.config import get_settings


async def check_balance_changing(user_id: str, balance_change: int) -> bool:
    status_info = {403: False, 200: True}
    url = get_settings().APPROVE_SERVICE_URL

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            params={
                "userId": user_id,
                "balanceChange": balance_change
            }
        )

        return status_info.get(response.status_code)

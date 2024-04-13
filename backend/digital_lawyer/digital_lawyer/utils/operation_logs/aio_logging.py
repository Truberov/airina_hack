import aiofiles

from balance.config import get_settings


async def write_operation_log(timestamp, data) -> None:
    filepath = get_settings().LOG_FILEPATH
    log_massage = f"{timestamp} - {data}\n"
    async with aiofiles.open(filepath, mode='a') as f:
        await f.write(log_massage)

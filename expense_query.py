import binascii

import hmac
import json
from datetime import datetime
from hashlib import sha1
from typing import Dict, Any, List, Union
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from aiohttp import ClientSession
import asyncio


USER_AGENT = "User-Agent': 'Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1 uni-app Html5Plus/1.0 (Immersed/35.555553)"

@dataclass_json
@dataclass
class Record:
    ts: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat
        )
    )
    amount: float
    balance_before: float
    balance_after: float
    description: str 
    device: str 
    type: str

    @staticmethod
    def parse(record: Dict):
        date = int(record['transdate'])
        time = int(record['transtime'])
        ts = datetime(year=int(date / 10000), month=int(date / 100 % 100), day=int(date % 100),
            hour=int(time / 10000), minute=int(time / 100 % 100), second=int(time % 100))
        
        return Record(ts=ts, amount=record['amount'], type=record['transflag'], \
            balance_before=record['cardbefbal'], balance_after=record['cardaftbal'], \
            description=record['transname'], device=record['devicename'])

@dataclass_json
@dataclass
class Transactions:
    account: str
    customer_id: int
    records: List[Record]

    @staticmethod
    def parse(account: str, result: Dict[str, Any]):
        if result['retcode'] == 0:
            transaction_list = json.loads(result['retdata'])
            customer_id = None if len(transaction_list) == 0 else transaction_list[0]['custid']

            transaction_list: List[Record] = [Record.parse(x) for x in transaction_list]
            return Transactions(account=account, customer_id=customer_id, records=transaction_list)

        return Transactions(None, None, [])

HEADERS: Dict[str, str] = {
    'User-Agent': USER_AGENT,
    'Content-Type': 'text/plain',
}

def format_time(t: datetime) -> str:
    return t.strftime(r'%Y%m%d%H%M%S')


def sign(account: str, start_time: str, end_time: str, ts: str) -> str:
    """ Generate sign parameter """ 
    def make_digest(message, key):
        """ HMAC digest algorithm """
        key = bytes(key, 'UTF-8')
        message = bytes(message, 'UTF-8')
        
        digester = hmac.new(key, message, sha1)
        signature1: bytes = digester.digest()
        signature2: bytes = binascii.b2a_hex(signature1)
        return signature2.decode('UTF-8')

    e: str = account
    a: str = start_time
    o: str = end_time
    i: str = ts

    message = e + a + o + i
    return make_digest(message, 'adc4ac6822fd462780f878b86cb94688')


async def query_transactions_without_retry(
    session: ClientSession,
    account: str, 
    start_time: Union[datetime, str], 
    end_time: Union[datetime, str],
):
    ts: str = format_time(datetime.now())
    if isinstance(start_time, str):
        start = start_time
    else: 
        start: str = format_time(start_time)

    if isinstance(end_time, str):
        end = end_time
    else:
        end: str = format_time(end_time)

    sign_hash = sign(account, start, end, ts)

    params: Dict[str, str] = {
        'endtime': end,
        'sign': sign_hash,
        'sign_method': 'HMAC',
        'starttime': start,
        'stuempno': account,
        'timestamp': ts
    }

    response = await session.post(
        url='https://xgfy.sit.edu.cn/yktapi/services/querytransservice/querytrans', 
        params=params,
    )
    response.raise_for_status()

    return Transactions.parse(account, await response.json())

async def query_expense(account: str)->str:
    async with ClientSession(headers=HEADERS) as session:
        results = await query_transactions_without_retry(
            session=session,
            account=account,
            start_time=datetime(year=2010, month=1, day=1),
            end_time=datetime.now(),
        )
        return json.dumps(
            obj=results.to_dict(),
            ensure_ascii=False,
            indent=4,
        )

__all__ = ['query_expense']
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException

from database.model.transaction import get_transaction_manager, Transaction, TransactionManager

router = APIRouter()

@router.get("/transaction/batch/unfinished")
def get_tr_unfinished(tr_manager: TransactionManager = Depends(get_transaction_manager)):
    tr: List[Transaction] = tr_manager.get_transactions_unfinished()
    return tr

@router.get("/transaction/batch/state/{order_status}")
def get_tr_state(order_status: int, tr_manager: TransactionManager = Depends(get_transaction_manager)):
    if order_status < 1 or order_status > 4:
        raise HTTPException(status_code=400, detail="Wrong order_status code.")
    tr: List[Transaction] = tr_manager.get_transactions_by_status(order_status)
    return tr

@router.get("/transaction/detail/{bid_uuid}")
def get_tr_detail(bid_uuid: str, tr_manager: TransactionManager = Depends(get_transaction_manager)):
    tr: Optional[TransactionManager] = tr_manager.get_transaction_by_bid_uuid(bid_uuid)
    if tr is None:
        raise HTTPException(status_code=404, detail="No such transaction with bid_uuid found.")
    return tr


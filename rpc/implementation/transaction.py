
import grpc
from grpc import ServicerContext
from database.model.transaction import TransactionManager
from database.model.admin import AdminManager

from tetherhelix_grpc.transaction_pb2 import TransactionRequest, ScopedTransactionRequest, TransactionsResponse, TransactionData
from tetherhelix_grpc.transaction_pb2_grpc import TransactionServicer

from util.logger import Logger

class MyTransactionServicer(TransactionServicer):
    def __init__(self) -> None:
        super().__init__()
        self.transaction_manager = TransactionManager()
        self.admin_manager = AdminManager()

    def GetCurrentTransactions(self, request: TransactionRequest, context: ServicerContext):
        """1. 현재 보유 포지션 조회 bot 및 front가 둘다 요청 가능 (단일 요청-응답)
        """
        if not self.admin_manager.check_authenicated(request.db_auth):
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details("Failed to authenticate")
        transactions = self.transaction_manager.get_transactions_unfinished(request.order_by)
        Logger.get_logger().info(f"GetCurrentTransactions : Sample len({len(transactions)})")
        context.set_code(grpc.StatusCode.OK)
        return TransactionsResponse(transactions=transactions)

    def GetPastTransactions(self, request: ScopedTransactionRequest, context: ServicerContext):
        """2. 과거 포지션 내역 조회 (단일 요청-응답)
        """
        transactions = [TransactionData(**dto) for dto in self.transaction_manager.get_transaction_by_timescope(request.start_time, request.end_time)]
        context.set_code(grpc.StatusCode.OK)
        return TransactionsResponse(transactions=transactions)

    def BidPlaced(self, request, context):
        """3. bot에서 기존에 불렀던 함수들 재추가
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BidFilled(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AskPlaced(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AskFilled(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def OrderFailedAfterBidPlaced(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def OrderFailedAfterAskPlaced(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')
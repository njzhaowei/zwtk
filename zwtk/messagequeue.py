import queue
import threading
import time
from typing import Any, Optional
from dataclasses import dataclass
from enum import Enum

class MessagePriority(Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3

@dataclass
class Message:
    id: str
    content: Any
    priority: MessagePriority = MessagePriority.NORMAL
    timestamp: float = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()

class SimpleMessageQueue:
    """

    .. code-block:: Python
    
        from messagequeue import SimpleMessageQueue, Message
        msg_queue = SimpleMessageQueue()
        def put_msg(msg):
            global msg_queue

            if not msg_queue.put(Message(
                id=uuid.uuid4(),
                content=msg,
            )):
                print("队列已满，无法发送消息")
        
        def get_msg():
            global msg_queue
            message = msg_queue.get(timeout=1)
            return message
    
    """
    def __init__(self, max_size: int = 10000):
        # 使用优先级队列
        self._queue = queue.PriorityQueue(maxsize=max_size)
        self._message_counter = 0
        self._lock = threading.Lock()
        
    def put(self, message: Message) -> bool:
        """向队列中添加消息"""
        try:
            # 根据优先级设置优先级值（数值越小优先级越高）
            priority_value = 3 - message.priority.value  # 反转优先级值
            
            # 使用优先级、时间戳和计数器作为元组，确保顺序
            with self._lock:
                self._message_counter += 1
                item = (priority_value, message.timestamp, self._message_counter, message)
            
            self._queue.put(item)
            return True
        except queue.Full:
            return False
    
    def get(self, timeout: float = None) -> Optional[Message]:
        """从队列中获取消息"""
        try:
            item = self._queue.get(timeout=timeout)
            # 返回消息对象
            return item[3]  # 元组的第四个元素是消息
        except queue.Empty:
            return None
    
    def task_done(self):
        """标记任务完成"""
        self._queue.task_done()
    
    def join(self):
        """等待所有任务完成"""
        self._queue.join()
    
    def size(self) -> int:
        """返回队列中的消息数量"""
        return self._queue.qsize()
    
    def empty(self) -> bool:
        """检查队列是否为空"""
        return self._queue.empty()
    
    def full(self) -> bool:
        """检查队列是否已满"""
        return self._queue.full()
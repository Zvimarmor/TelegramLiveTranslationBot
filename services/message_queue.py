# services/message_queue.py

from queue import Queue
import threading

# Global message queue: {group_id: Queue}
message_queues = {}
queue_lock = threading.Lock()  # Ensure thread-safe access to the queues

def add_to_queue(group_id, sender, message_text) -> bool:
    """
    Add a message to the queue for the specified group.
    
    Args:
        group_id (str): The ID of the group.
        sender (str): The ID of the sender.
        message_text (str): The text of the message.
    """
    with queue_lock:  # Ensure thread-safe access to the queue dictionary
        if group_id not in message_queues:
            message_queues[group_id] = Queue()
        
        # Add the message to the group's queue
        message_queues[group_id].put({
            "sender": sender,
            "message_text": message_text
        })

def get_from_queue(group_id) -> dict:
    """
    Get the next message from the queue for the specified group.
    
    Args:
        group_id (str): The ID of the group.
    
    Returns:
        dict: The next message in the group's queue, or None if the queue is empty.
    """
    with queue_lock:  # Ensure thread-safe access to the queue dictionary
        if group_id in message_queues and not message_queues[group_id].empty():
            return message_queues[group_id].get()
        return None

def get_queue_size(group_id) -> int:
    """
    Get the size of the queue for the specified group.
    
    Args:
        group_id (str): The ID of the group.
    
    Returns:
        int: The number of messages in the group's queue.
    """
    with queue_lock:  # Ensure thread-safe access to the queue dictionary
        if group_id in message_queues:
            return message_queues[group_id].qsize()
        return 0

def clear_queue(group_id) -> bool:
    """
    Clear the queue for the specified group.
    
    Args:
        group_id (str): The ID of the group.
    """
    with queue_lock:  # Ensure thread-safe access to the queue dictionary
        if group_id in message_queues:
            message_queues[group_id].queue.clear()  # Clear the queue
            del message_queues[group_id]  # Remove the queue from the dictionary
            return True
    return False

def peek_all_messages(group_id) -> list:
    """
    Peek at all messages in the queue for the specified group without removing them.
    
    Args:
        group_id (str): The ID of the group.
    
    Returns:
        list: A list of messages in the group's queue.
    """
    with queue_lock:  # Ensure thread-safe access to the queue dictionary
        if group_id in message_queues:
            return list(message_queues[group_id].queue)
        return []
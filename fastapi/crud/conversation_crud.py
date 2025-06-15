from typing import List, Optional, Dict
from models.conversation import Conversation
from datetime import datetime
import uuid


class ConversationCRUD:

    @staticmethod
    def create_conversation(conversation_id: Optional[str] = None) -> Conversation:
        """Create a new conversation"""
        if not conversation_id:
            conversation_id = str(uuid.uuid4())

        conversation = Conversation(
            id=conversation_id,
            messages=[],
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        conversation.save()
        print(f"🆕 Created new conversation: {conversation_id}")
        return conversation

    @staticmethod
    def get_conversation(conversation_id: str) -> Optional[Conversation]:
        """Get a conversation by ID"""
        try:
            conversation = Conversation.objects(id=conversation_id).first()
            if conversation:
                print(
                    f"📖 Found conversation: {conversation_id} with {len(conversation.messages)} messages"
                )
                return conversation
            print(f"❌ Conversation not found: {conversation_id}")
            return None
        except Exception as e:
            print(f"❌ Error getting conversation {conversation_id}: {e}")
            return None

    @staticmethod
    def get_or_create_conversation(
        conversation_id: Optional[str] = None,
    ) -> Conversation:
        """Get existing conversation or create new one"""
        if conversation_id:
            conversation = ConversationCRUD.get_conversation(conversation_id)
            if conversation:
                return conversation

        # Create new conversation
        return ConversationCRUD.create_conversation(conversation_id)

    @staticmethod
    def add_message(conversation_id: str, role: str, content: str) -> Conversation:
        """Add a message to a conversation"""
        conversation = ConversationCRUD.get_or_create_conversation(conversation_id)

        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
        }

        conversation.messages.append(message)
        conversation.updated_at = datetime.now()
        conversation.save()

        print(f"💾 Added {role} message to conversation {conversation_id}")
        print(f"📝 Conversation now has {len(conversation.messages)} messages")
        return conversation

    @staticmethod
    def get_messages(conversation_id: str) -> List[Dict]:
        """Get all messages from a conversation"""
        conversation = ConversationCRUD.get_conversation(conversation_id)
        if conversation:
            return conversation.messages
        return []

    @staticmethod
    def get_langchain_messages(conversation_id: str) -> List:
        """Convert conversation messages to LangChain format"""
        from langchain_core.messages import HumanMessage, AIMessage

        messages = ConversationCRUD.get_messages(conversation_id)
        langchain_messages = []

        for msg in messages:
            if msg["role"] == "user":
                langchain_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                langchain_messages.append(AIMessage(content=msg["content"]))

        return langchain_messages

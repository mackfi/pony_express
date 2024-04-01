import { useQuery } from "react-query";
import { Link, useParams } from "react-router-dom";
import SendMessage from "./SendMessage";

function ChatList({ chats }) {
    return (
      <>
        <div className="chat-list">
          {chats.map((chat) => (
            <ChatListItem key={chat.id} chat={chat} />
          ))}
        </div>
      </>
    )
  }

function ChatListItem({chat}) {
    return (
        <Link key={chat.id} to={`/chats/${chat.id}`} className="chat-list-item">
          <div className="chat-list-item-name">
            {chat.name}
          </div>
          <div className="chat-list-item-detail">
            {chat.user_ids.join(", ")}
          </div>
          <div className="chat-list-item-detail">
            Created at: {new Date(chat.created_at).toDateString()}
          </div>
        </Link>
      )
}

export default ChatList;
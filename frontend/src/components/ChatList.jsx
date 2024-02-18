import { useQuery } from "react-query";
import { Link, useParams } from "react-router-dom";

function ChatList({ chats }) {
    return (
      <div className="chat-list">
        {chats.map((chat) => (
          <ChatListItem key={chat.id} chat={chat} />
        ))}
      </div>
    )
  }

function ChatListItem({chat}) {
    return (
        <Link key={chat.id} to={`/chats/${chat.id}`} className="chat-list-item">
          <div className="chat-list-item-name">
            {chat.name}
          </div>
          <div className="chat-list-item-detail">
            {chat.user_ids.map((user) => (
                <div key={user.id}> {user} </div>
            ))}
          </div>
          <div className="chat-list-item-detail">
            Created at: {chat.created_at}
          </div>
        </Link>
      )
}

export default ChatList;
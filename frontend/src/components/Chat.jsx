import { useQuery } from "react-query";
import { Link, useParams } from "react-router-dom";
import "./ChatsPage.css";

function Chat({chat}) {

    const { data } = useQuery({
        queryKey: ["chat", chat.id],
        queryFn: () => (
          fetch(`http://127.0.0.1:8000/chats/${chat.id}/messages`)
            .then((response) => response.json())
        ),
      });
      if (data && data.messages) {
        return (
        <div className="message-list">
        {data.messages.map((message) => (
            <div key={message.id} className="message-card"> 
            <div className="message-header">
             <div className="message-user">{message.user_id} </div>
             <div className="message-details">{new Date(message.created_at).toDateString()} - {new Date(message.created_at).toLocaleTimeString()} </div>
             </div>
             <div className="message-text">{message.text} </div>
            </div>
          ))}
        </div>
        )
      }
}

function ChatCardQueryContainer({ chatId }) {
    const { data } = useQuery({
      queryKey: ["chats", chatId],
      queryFn: () => (
        fetch(`http://127.0.0.1:8000/chats/${chatId}`)
          .then((response) => response.json())
      ),
    });
  
    if (data && data.chat) {
      return <ChatCardContainer chat={data.chat} />
    }
  
    return <h2>loading...</h2>
  }

  function ChatCardContainer({ chat }) {
    return (
      <div className="chat-card-container">
        <h2 className="col-header">{chat.name}</h2>
        <Chat chat={chat} />
      </div>
    );
  }

export default ChatCardQueryContainer;
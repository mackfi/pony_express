import { useQuery } from "react-query";
import { Link, useParams } from "react-router-dom";
import "./ChatsPage.css";

function Chat({chat}) {

    const { data } = useQuery({
        queryKey: ["chats"],
        queryFn: () => (
          fetch(`http://127.0.0.1:8000/chats/${chat.id}/messages`)
            .then((response) => response.json())
        ),
      });
      if (data && data.messages) {
        return (
        <div className="message-list">
        {data.messages.map((message) => (
            <div key={message.id}> {message.text} </div>
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
        <h2>{chat.name}</h2>
        <Chat chat={chat} />
      </div>
    );
  }

export default ChatCardQueryContainer;
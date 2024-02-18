import { useQuery } from "react-query";
import { Link, useParams } from "react-router-dom";
import "./ChatsPage.css";
import ChatList from "./ChatList";
import ChatCardQueryContainer from "./Chat"

function ChatsPage() {
    const { chatId } = useParams();
    return (
      <div className="chats-page">
        <ChatListContainer />
        {chatId ? <ChatCardQueryContainer chatId={chatId} /> : <h2>pick a chat</h2>}
      </div>
    );
}

function ChatListContainer() {

    const { data } = useQuery({
        queryKey: ["chats"],
        queryFn: () => (
          fetch("http://127.0.0.1:8000/chats")
            .then((response) => response.json())
        ),
      });
    
      if (data?.chats) {
        return (
          <div className="chat-list-container">
            <h2>chats</h2>
            <ChatList chats={data.chats} />
          </div>
        )
      }
    
      return (
        <h2>chat list</h2>
      );
}

export default ChatsPage;
import { useQuery } from "react-query";
import { Link, useParams } from "react-router-dom";
import "./ChatsPage.css";
import ChatList from "./ChatList";
import ChatCardQueryContainer from "./Chat"
import LeftNav from "./LeftNav";
import SendMessage from "./SendMessage";

function ChatsPage() {
    const { chatId } = useParams();
    return (
      <div className="chats-page">
        <LeftNav />
        {chatId ? <><ChatCardQueryContainer chatId={chatId} /></>: <h2 className="col-header">select a chat</h2>}
        {/* <ChatListContainer />
        {chatId ? <ChatCardQueryContainer chatId={chatId} /> : <h2 className="col-header">select a chat</h2>} */}
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
          <a href="/chats" className="nav-link"><h2 className="col-header nav-link">chats</h2></a>
            <ChatList chats={data.chats} />
          </div>
        )
      }
    
      return (
        <a href="/chats" className="nav-link"><h2 className="col-header nav-link">chats</h2></a>
      );
}

export default ChatsPage;
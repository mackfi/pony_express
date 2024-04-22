import { useState } from "react";
import { useMutation, useQueryClient } from "react-query";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/auth";
import Button from "./Button";

const baseUrl = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

function Input(props) {
  return (
    <div className="flex flex-col py-2">
      <label className="text-s text-gray-400" htmlFor={props.name}>
        {props.name}
      </label>
      <input
        {...props}
        className="border rounded bg-transparent px-2 py-1"
      />
    </div>
  );
}

function SendMessage({chatId}) {
  const queryClient = useQueryClient();
  const navigate = useNavigate();
  const { token } = useAuth();
  const [name, setName] = useState("");

  const mutation = useMutation({
    mutationFn: () => (
      fetch(
        baseUrl+`/chats/${chatId}/messages`,
        {
          method: "POST",
          headers: {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            "text": name,
          }),
        },
      ).then((response) => response.json())
    ),
    onSuccess: (data) => {
      queryClient.invalidateQueries({
        queryKey: ["chats"],
      });
      navigate(`/chats/${chatId}`);
      // alternatively, we could "reset" the form
    },
  });

  const onSubmit = (e) => {
    e.preventDefault();
    mutation.mutate();
  };

  return (
    <form onSubmit={onSubmit}>
      <Input
        name="new message"
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <Button type="submit">send</Button>
    </form>
  );
}


export default SendMessage;
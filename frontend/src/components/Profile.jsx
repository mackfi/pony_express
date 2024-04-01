import { useEffect, useState } from "react";
import { useAuth } from "../context/auth";
import { useUser } from "../context/user";
import Button from "./Button";
import FormInput from "./FormInput";
import { useMutation, useQueryClient } from "react-query";
import { useNavigate } from "react-router-dom";

function Error({ message }) {
    if (message === "") {
      return <></>;
    }
    return (
      <div className="text-red-300 text-xs">
        {message}
      </div>
    );
  }

function Profile() {
  const { logout } = useAuth();
  const { token } = useAuth();
  const user = useUser();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [readOnly, setReadOnly] = useState(true);
  const [error, setError] = useState("");
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  const reset = () => {
    if (user) {
      setUsername(user.username);
      setEmail(user.email);
    }
  }

  useEffect(reset, [user]);

  const onSubmit = (e) => {
    e.preventDefault();
    console.log("username: " + username);
    console.log("email: " + email);
    setReadOnly(true);
    mutation.mutate();
  }

  const onClick = () => {
    setReadOnly(!readOnly);
    reset();
  };

  const mutation = useMutation({
    mutationFn: () => (
      fetch(
        `http://127.0.0.1:8000/users/me`,
        {
          method: "PUT",
          headers: {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            "username": username,
            "email": email,
          }),
        },
      )//.then((response) => response.json())
    ),
    onError: (data) => {
        setError("Couldn't update name/email. Choose a unique name/email that doesn't already exist.")
    },
    onSuccess: (data) => {
      setError("")
      queryClient.invalidateQueries({
        queryKey: ["users"],
      });
      navigate(`/profile/`);
    },
  });

  return (
    <div className="max-w-96 mx-auto px-4 py-8">
      <h2 className="text-2xl font-bold py-2">
        details
      </h2>
      <form className="border rounded px-4 py-2" onSubmit={onSubmit}>
        <FormInput
          name="username"
          type="text"
          value={username}
          readOnly={readOnly}
          setter={setUsername}
        />
        <FormInput
          name="email"
          type="email"
          value={email}
          readOnly={readOnly}
          setter={setEmail}
        />
        {!readOnly &&
          <Button className="mr-8" type="submit">
            update
          </Button>
        }
        <Button type="button" onClick={onClick}>
          {readOnly ? "edit" : "cancel"}
        </Button>
      </form>
      <Error message={error} />
      <Button onClick={logout}>
        logout
      </Button>
    </div>
  );
}

export default Profile;
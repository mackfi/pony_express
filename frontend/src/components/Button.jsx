function Button(props) {
    const className = [
      props.className || "",
      "border rounded",
      "px-4 py-2 my-4",
      props.disabled ?
        "bg-rose-400 italic" :
        "border-lgrn bg-transparent hover:bg-emerald-800",
    ].join(" ");
  
    return (
      <button {...props} className={className}>
        {props.children}
      </button>
    );
  }
  
  export default Button;
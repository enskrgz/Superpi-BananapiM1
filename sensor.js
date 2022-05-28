const io = require("socket.io")(5000);


io.on("connection", socket => {
  // either with send()
  console.log('Connected');
  socket.send("Hello!");

  // handle the event sent with socket.send()
  socket.on("fromAPI", (data) => {
    console.log(data);
    socket.emit("fromAPI", data);

  });

     });
});

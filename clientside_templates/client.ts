import { io, Socket } from "socket.io-client";

// Replace with the actual username, e.g., from a template or input
const username = "your_username";

// Connect and send username as auth data
const socket: Socket = io("http://localhost:5000", {
    auth: { username }
});

// Listen for the updated user list
socket.on("update_users", (users: string[]) => {
    console.log("Connected users:", users);
    // Update your UI here
});

// Optional: handle disconnect
socket.on("disconnect", () => {
    console.log("Disconnected from server");
});
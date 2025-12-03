# Py Chat

## Plan

### Phase 1: Basic WebSocket Connection

Goal: Get a connection working between one client and server

Set up a basic WebSocket server that accepts connections
Create a simple HTML page with JavaScript that connects to your server
Make the connection print "connected" on both sides
Test disconnection handling—close the browser tab and verify the server notices

Success metric: You can open your browser, connect to the server, and see confirmation messages on both ends.

### Phase 2: Echo Server

Goal: Send messages from client to server and back

Add a text input and send button to your HTML page
Send whatever the user types to the server through the WebSocket
Have the server receive the message and send it back to the same client
Display received messages on the page

Success metric: You type "hello" in the browser, hit send, and see it appear on the page (echoed back from the server).

### Phase 3: Two Clients Talking

Goal: Messages from one client reach another client

Modify server to track multiple connected clients in a list
When a message comes in, send it to all connected clients (not just the sender)
Open two browser tabs and verify messages sent from one appear in the other
Handle the case where you might want to exclude the sender from the broadcast (or not—your choice)

Success metric: Open two browser tabs, send a message from one, see it appear in both.

### Phase 4: User Identity

Goal: Know who sent each message

Add a simple username prompt when someone first connects
Send the username to the server as the first message after connecting
Store username with each connection in your server's connection list
Include the username in every message broadcast so clients can display "Alice: hello"

Success metric: Messages show who sent them, like "Alice: hello" and "Bob: hi there"

### Phase 5: Basic Database Integration

Goal: Persist messages so they survive server restarts

Set up a simple SQLite database with a messages table (id, sender, recipient, content, timestamp)
When a message comes in, save it to the database before broadcasting
When a user connects, load and send them recent message history
Test by restarting the server and verifying messages are still there

Success metric: Stop the server, restart it, reconnect—previous messages are still visible.

### Phase 6: Direct Messaging Logic

Goal: Send messages to specific users, not everyone

Add recipient information to messages—each message specifies who it's for
Modify server broadcast logic to only send to the intended recipient (and sender for confirmation)
Create a UI element for selecting who to message (could be a dropdown or simple text input)
Store recipient info in the database

Success metric: Three people connected—Alice messages Bob, Carol doesn't see it.

### Phase 7: Conversation Threads

Goal: Organize messages into conversations between two people

When loading history, only load messages between the current user and their selected conversation partner
Create a conversation list UI showing who you can message
When you click a person, load your conversation with them
Implement unread message indicators (count messages where recipient is you and you haven't seen them yet)

Success metric: You can switch between conversations with different people and see the right message history for each.

### Phase 8: Authentication

Goal: Replace username prompts with proper login

Create a simple registration/login page (HTTP, not WebSocket)
Use sessions or JWT tokens to identify users
Verify the token when someone connects via WebSocket
Associate WebSocket connections with authenticated user IDs

Success metric: Users must log in before chatting, and the system correctly identifies them.

### Phase 9: Polish & Edge Cases

Goal: Handle real-world scenarios gracefully

Show "user is typing" indicators
Display online/offline status
Handle reconnection when someone's internet drops temporarily
Add message timestamps to the UI
Improve error messages and loading states
Test with spotty internet connections

Success metric: App feels responsive and handles network issues without breaking.

### Phase 10: Deployment

Goal: Make it accessible online

Deploy server to a hosting platform (Heroku, DigitalOcean, Railway, etc.)
Set up proper WebSocket support (some hosts need special configuration)
Deploy your database (or use a hosted database)
Get HTTPS working (required for secure WebSocket connections—wss://)
Test with friends on different networks

Success metric: You and a friend can chat from different locations over the internet.

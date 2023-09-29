from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Replace these placeholders with your database credentials
db_host = 'localhost'      # Your MySQL host address
db_user = 'yashstar_ai'    # Your MySQL username
db_password = 'yashstar_ai'  # Your MySQL password
db_name = 'yashstar_ai'    # Your MySQL database name

# Connect to the MySQL database
conn = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)

# Function to create the chat_logs table if it doesn't exist
def create_chat_logs_table():
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_message TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()

# Call the function to create the table when the app starts
create_chat_logs_table()

# Define a route to serve the chatbot.html file
@app.route('/')
def serve_html():
    return app.send_static_file('chatbot.html')

# Define a route to handle incoming chat messages
@app.route('/chat', methods=['POST'])
def chat():
    # Get the user's message from the request JSON
    user_message = request.json.get('userMessage')
    
    # Simulate a bot response based on the user's message
    bot_response = simulate_chatbot_response(user_message)

    # Insert the conversation into the database
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO chat_logs (user_message, bot_response) VALUES (%s, %s)
    ''', (user_message, bot_response))
    
    # Commit the changes to the database
    conn.commit()

    # Return the bot's response as JSON
    return jsonify({"botResponse": bot_response})

# Function to simulate bot responses based on user messages
def simulate_chatbot_response(user_message):
    if 'hello' in user_message:
        return "Hello! How can I assist you today?"
    elif 'complaint' in user_message:
        return "I'm sorry to hear that. Please provide more details about your complaint."
    else:
        return "I'm here to help! Feel free to ask any questions."

# Start the Flask web server in debug mode
if __name__ == '__main__':
    app.run(debug=True)

import pyautogui
import time
import pyperclip
from openai import OpenAI
import keyboard  # pip install keyboard

# Enable PyAutoGUI fail-safe (move mouse to top-left corner to stop)
pyautogui.FAILSAFE = True

# Set up the Groq API client
client = OpenAI(
    api_key="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",
    base_url="https://api.groq.com/openai/v1"  # Groq API endpoint
)

def is_last_msg_from_sender(chat_log, sender_name=""):
    """
    Check if the last message in chat is from the sender (not from Zainul)
    Returns True if we should respond, False if we shouldn't
    """
    if not chat_log.strip():
        return False
    
    # Split by date pattern and get the last message
    messages = chat_log.strip().split("] ")
    
    if len(messages) < 2:
        return False
    
    # Get the last message (after the last timestamp)
    last_msg = messages[-1]
    
    # Check if the last message is from Zainul (the bot)
    # If it starts with "Zainul:" or contains bot name, don't respond
    if last_msg.startswith("Zainul:") or "Zainul:" in last_msg.split('\n')[0]:
        return False
    
    # If sender_name is provided, check if last message is from that sender
    if sender_name and sender_name in last_msg:
        return True
    
    # If no sender name provided, assume any non-Zainul message needs response
    return True

# Store the last processed message to avoid duplicate responses
last_processed_chat = ""

# Step 1: Click to open app
pyautogui.click(1180, 1047)    
time.sleep(2)  # wait for app to open            

print("Bot starting... Press 'q' to quit or move mouse to top-left corner")
print("Bot will start in 3 seconds...")
time.sleep(3)

while True:
    try:
        # Check for quit key
        if keyboard.is_pressed('q'):
            print("Stopping bot...")
            break
        # Step 2: Select text
        pyautogui.moveTo(896, 265)
        pyautogui.mouseDown()
        pyautogui.moveTo(1897, 1003, duration=1)  # drag smoothly
        pyautogui.mouseUp()
        time.sleep(0.5)

        # Step 3: Copy to clipboard
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.5)
        pyautogui.click(889, 329)

        # Step 4: Get text from clipboard
        chat_history = pyperclip.paste()
        
        # Skip if chat hasn't changed (prevents duplicate responses)
        if chat_history == last_processed_chat:
            print("No new messages, waiting...")
            time.sleep(2)
            continue
        
        print("Copied Text:\n", chat_history)
        
        # Check if we should respond
        if not is_last_msg_from_sender(chat_history):
            print("Last message is from bot or no response needed")
            time.sleep(2)
            continue
        
        print("New message detected, generating response...")
        
        # Step 5: Send to Groq API with better prompt
        response = client.chat.completions.create(
            model="llama3-70b-8192",  # ✅ Use correct model name
            messages=[
                {
                    "role": "system",
                    "content": ("You are a person named Zainul who speaks Hindi as well as English. "
                              "You are from India. You analyze chat history and respond like Zainul. "
                              "Output should be the next chat response (text messages only). "
                              "Keep responses natural and conversational.")
                },
                {
                    "role": "user",
                    "content": chat_history
                }
            ]
        )

        # Step 6: Handle and paste the response
        response_text = response.choices[0].message.content
        print("AI Response:", response_text)
        
        # Store current chat as processed
        last_processed_chat = chat_history
        
        pyperclip.copy(response_text)

        # Step 7: Paste response and send
        pyautogui.click(1151, 960)
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(2)  # Wait before next iteration
        
    except Exception as e:
        print(f"Error occurred: {e}")
        time.sleep(5)  # Wait before retrying
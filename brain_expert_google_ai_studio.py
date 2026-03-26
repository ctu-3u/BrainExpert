from google import genai
import sys
import os

# --- CONFIGURATION ---
API_KEY = os.getenv("GOOGLE_AI_API_KEY", "")
# ---------------------

if not API_KEY:
    print("ERROR: Google AI API Key is missing.\n")
    print("To run this Brain Expert AI, you must specify your API key.")
    print("You can do this in one of two ways:\n")
    
    print("1. Set an Environment Variable (Recommended)")
    print("   Windows (CMD):  set GOOGLE_AI_API_KEY=your-actual-api-key")
    print("   Windows (PS):   $env:GOOGLE_AI_API_KEY='your-actual-api-key'")
    print("   Mac/Linux:      export GOOGLE_AI_API_KEY=your-actual-api-key\n")
    
    print("2. Get your API key from: https://aistudio.google.com/app/apikey\n")
    sys.exit(1)

print("Initializing Brain Expert AI...")

# 1. Initialize the client with API key
try:
    # Initialize google.genai client with API key for REST-based access
    client = genai.Client(api_key=API_KEY) 
    # client = genai.Client() # automatically get key form the environment variable `GEMINI_API_KEY`.
except Exception as e:
    print(f"\nError initializing client: {e}")
    sys.exit(1)


# 2. Define the exact format with per-example references
format_rules = """
You are an expert neuroscientist with comprehensive knowledge of all brain parcellations, including classical (Brodmann) and modern definitions (e.g., HCP-MMP1, Glasser 2016). 

If a user provides a short code, interpret it as a specific brain area within a known atlas rather than assuming it is a typo.

1. Name: [Name of the area. If the response language is NOT English, you MUST include the English name in parentheses after the localized name, e.g., "海马体 (Hippocampus)"]
2. Categorization Method: [e.g., Anatomical, Cytoarchitectural/Brodmann, Functional, or Connectome-based]
3. Location: [Brief description of where it is]
4. Primary Function: [1-2 sentences explaining what it does]

5. Illustrations & Functional Examples:
[List as many distinct functional examples as you can find. Label them 5.a, 5.b, etc. As many as possible.]
   5.a. [Describe a specific scenario or function]
        Source: [Provide a citation (Author, Year), a scientific paper URL, or a reliable webpage URL]
   5.b. [Describe next scenario]
        Source: [Provide source]
   ...

6. Associated Disorders: [List several related conditions]

If the user asks a follow-up question, answer normally in the same language as the question (limited to English, Chinese, or Hindi), keeping the tone professional and concise.
"""

print("🧠 Brain Expert AI (Evidence-Based Mode)")
print("Type a brain area to start (e.g., 'Hippocampus'). Type 'q' or 'quit' or 'exit' to quit.\n")

# 3. Start the Chat Session
try:
    # Create a chat with the Gemini model using google.genai
    model_config = genai.types.GenerateContentConfig(
        system_instruction=format_rules,
        temperature=0.3,
    )
    
    chat = client.chats.create(
        model="gemini-3-flash-preview",
        config=model_config
    )
except Exception as e:
    print(f"\nError creating chat: {e}")
    sys.exit(1)

while True:
    try:
        user_input = input("You > ")
        
        clean_input = user_input.strip().lower()
        if clean_input in ['q', 'quit', 'exit']:
            print("Ending session. Goodbye!")
            break
            
        if not clean_input:
            continue
            
        print("Retrieving evidence-based information...\n")
        
        # 4. Send message to the CHAT session
        try:
            response = chat.send_message(user_input)
        except Exception as e:
            print(f"\nError: {e}\n")
            continue
        
        # 5. Print the formatted response
        print("=" * 50) 
        print(f"{response.text}\n")
        print("-" * 50) 
        
    except Exception as e:
        print(f"\nError: {e}\n")

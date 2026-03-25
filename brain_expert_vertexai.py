from google import genai
from google.genai import types
import sys
import os

# --- CONFIGURATION ---
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "YOUR_PROJECT_ID")
LOCATION = "us-central1"
# ---------------------

if PROJECT_ID == "YOUR_PROJECT_ID":
    print("ERROR: Google Cloud Project ID is missing.\n")
    print("To run this Brain Expert AI, you must specify your project ID.")
    print("You can do this in one of two ways:\n")
    
    print("Please set an Environment Variable (Recommended)")
    print("   Windows (CMD):  set GOOGLE_CLOUD_PROJECT=your-actual-project-id")
    print("   Windows (PS):   $env:GOOGLE_CLOUD_PROJECT='your-actual-project-id'")
    print("   Mac/Linux:      export GOOGLE_CLOUD_PROJECT=your-actual-project-id\n")
    sys.exit(1)

print(f"Initializing Brain Expert AI for project: {PROJECT_ID}...")

# 1. Initialize the client
# On your local machine, this will look for the credentials created 
# via 'gcloud auth application-default login'
try:
    client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location=LOCATION
    )
except Exception as e:
    print(f"\nError initializing client: {e}")
    print("Did you run 'gcloud auth application-default login'?")
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
chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction=format_rules,
        temperature=0.3,
    )
)

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
        response = chat.send_message(user_input)
        
        # 5. Print the formatted response
        print("=" * 50) 
        print(f"{response.text}\n")
        print("-" * 50) 
        
    except Exception as e:
        print(f"\nError: {e}\n")
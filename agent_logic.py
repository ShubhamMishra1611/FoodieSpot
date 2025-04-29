import json
import datetime
import os
from dotenv import load_dotenv
from groq import Groq # Import Groq library
from tools import AVAILABLE_TOOLS, TOOL_DESCRIPTIONS

load_dotenv()
groq_api_key = os.environ.get("GROQ_API_KEY")

if not groq_api_key:
    print("ERROR: GROQ_API_KEY not found in environment variables.")
    print("Please create a .env file with GROQ_API_KEY=your_key")
    

client = Groq(api_key=groq_api_key) if groq_api_key else None
LLM_MODEL = "llama3-8b-8192"

# --- LLM Interaction using Groq API ---
def call_groq_llm(prompt_messages):
    """
    Calls the Groq API with the provided messages structured for chat completion.
    Returns the string content of the assistant's reply.
    """
    if not client:
        print("ERROR: Groq client not initialized due to missing API key.")
        # Fallback to a simple message instead of crashing
        return json.dumps({"tool_name": "none", "response": "Sorry, the AI service is not configured correctly (API key missing). Please contact support."})

    try:
        print("\n--- Sending Prompt to Groq LLM ---")
        print("--- End Prompt ---")

        chat_completion = client.chat.completions.create(
            messages=prompt_messages,
            model=LLM_MODEL,
            temperature=0.1, 
            max_tokens=500,  # Adjust as needed
            # We are NOT using Groq's native tool_choice/tools here
            # We instruct the LLM via the system prompt to return JSON
        )

        response_content = chat_completion.choices[0].message.content
        print(f"\n--- Raw LLM Response ---")
        print(response_content)
        print(f"--- End Raw LLM Response ---")
        return response_content

    except Exception as e:
        print(f"ERROR: Groq API call failed: {e}")
        error_response = {
            "tool_name": "none",
            "response": f"Sorry, I encountered an error trying to reach the AI service ({type(e).__name__}). Please try again later."
        }
        return json.dumps(error_response)


def process_user_message(user_message, conversation_history):
    """
    Main function to handle user input, interact with LLM, and execute tools.
    Now uses the real Groq API call and robust JSON parsing.
    """
    # 1. Construct Prompt Messages for LLM (Chat Format)
    system_prompt = f"""
You are FoodieBot, a helpful assistant for booking tables at FoodieSpot restaurants.
Be concise and helpful. Use the available tools to answer user requests about finding restaurants and making reservations.
If you need to ask clarifying questions, do so. Today's date is {datetime.date.today().isoformat()}.

Available Tools Description:
{TOOL_DESCRIPTIONS}

Instructions:
Analyze the user's request based on the conversation history.
Determine the user's intent. If a tool can fulfill the request, respond ONLY with a single JSON object containing the 'tool_name' and 'arguments'. Use the exact tool names and parameter names described above.
If no tool is needed, or you need to ask a clarifying question, respond ONLY with a single JSON object like: {{"tool_name": "none", "response": "Your natural language response here."}}
Ensure all required parameters for a tool call are extracted from the conversation or the user message. Ask for clarification if essential parameters are missing for a required tool. Do not make up information.
Respond only with the JSON object, nothing else.
"""

    messages = [
        {"role": "system", "content": system_prompt}
    ]
    # Add history turns - simple split approach, needs refinement for robustness
    history_turns = conversation_history.strip().split('\n')
    for turn in history_turns:
        # parsing history string prefixes
        if turn.startswith("User:"):
             messages.append({"role": "user", "content": turn[len("User:"):].strip()})
        elif turn.startswith("Assistant:"):
             messages.append({"role": "assistant", "content": turn[len("Assistant:"):].strip()})
        
    messages.append({"role": "user", "content": user_message})


    llm_response_raw = call_groq_llm(messages) 

    
    llm_response_dict = None 
    tool_name = None
    arguments = None
    direct_response = None
    cleaned_response_raw = llm_response_raw 

    try:
        
        if llm_response_raw.startswith("```json"):
            cleaned_response_raw = llm_response_raw[7:-3].strip()
        else:
            
            cleaned_response_raw = llm_response_raw.strip()

        
        llm_response_dict = json.loads(cleaned_response_raw)

        
        if isinstance(llm_response_dict, dict):
            tool_name = llm_response_dict.get("tool_name")
            arguments = llm_response_dict.get("arguments")
            direct_response = llm_response_dict.get("response")
            
            if tool_name and tool_name != "none" and direct_response:
                 print(f"Warning: LLM returned both tool_name '{tool_name}' and direct_response. Prioritizing tool call.")
                 direct_response = None 
            
            elif tool_name == "none" and direct_response is None:
                 print(f"Warning: LLM returned tool_name 'none' but no 'response' field. Treating raw as response.")
                 direct_response = cleaned_response_raw 
                 tool_name = "none" 

        else:
            print(f"Warning: LLM returned valid JSON, but not the expected dictionary format: {llm_response_dict}")
            direct_response = cleaned_response_raw 
            tool_name = "none"

    except json.JSONDecodeError:
        
        print(f"Warning: Could not decode LLM response as JSON, treating as direct response: '{cleaned_response_raw}'")
        direct_response = cleaned_response_raw 
        tool_name = "none"

    
    
    if tool_name == "none" and not direct_response:
        
        print(f"Error: tool_name is 'none' but direct_response is empty/None. Raw: '{llm_response_raw}'")
        direct_response = "Sorry, I received an empty response. Could you please try again?"
        
        tool_name = "none"


    
    updated_history = conversation_history 

    if tool_name and tool_name != "none":
        if tool_name in AVAILABLE_TOOLS:
            tool_function = AVAILABLE_TOOLS[tool_name]
            try:
                
                tool_args = arguments if arguments is not None else {}
                print(f"--- Executing Tool: {tool_name} with args: {tool_args} ---")
                tool_result = tool_function(**tool_args) 
                print(f"--- Tool Result: {tool_result} ---")

                
                if tool_name == "search_restaurants":
                    if not tool_result:
                        response_to_user = "I couldn't find any restaurants matching your criteria."
                    else:
                        response_lines = ["I found these options:"]
                        for r in tool_result:
                            availability_info = ""
                            if r.get('availability_checked'):
                                availability_info = " (Available at requested time)" if r.get('is_available_at_request') else " (Not Available at requested time)"
                            
                            cuisine_str = ""
                            if isinstance(r.get('cuisine'), list):
                                cuisine_str = ', '.join(r['cuisine'])
                            elif isinstance(r.get('cuisine'), str):
                                cuisine_str = r['cuisine']

                            response_lines.append(f"- {r.get('name', 'N/A')} ({r.get('location_area', 'N/A')}, {cuisine_str}) - ID: {r.get('id', 'N/A')}{availability_info}")
                        
                        response_to_user = "\n".join(response_lines)
                        if len(tool_result) > 0:
                             response_to_user += "\n\nDo any of these look good? Please provide the ID (e.g., FS01) to check specific times or make a booking."

                elif tool_name == "make_reservation":
                    if tool_result.get("success"):
                        details = tool_result.get('details', {})
                        response_to_user = f"Booking confirmed! Your reservation at {details.get('restaurant_name', 'the restaurant')} for {details.get('party_size', 'N/A')} people on {details.get('date', 'N/A')} at {details.get('time', 'N/A')} is set. Your Booking ID is {details.get('booking_id', 'N/A')}."
                    else:
                        response_to_user = f"Sorry, I couldn't complete the booking. Reason: {tool_result.get('reason', 'Unknown error')}"

                else: 
                     response_to_user = f"Action {tool_name} completed. Result: {json.dumps(tool_result)}"

                
                updated_history = conversation_history + f"\nUser: {user_message}\nAssistant: {response_to_user}"
                return response_to_user, updated_history

            except TypeError as e:
                  print(f"ERROR: Tool '{tool_name}' called with incorrect arguments: {arguments}. Error: {e}")
                  response_to_user = f"Sorry, I seem to have the wrong details to {tool_name.replace('_', ' ')}. Could you please provide the required information again?"
                  updated_history = conversation_history + f"\nUser: {user_message}\nAssistant: {response_to_user}" 
                  return response_to_user, updated_history

            except Exception as e:
                print(f"ERROR: Failed to execute tool {tool_name} with args {arguments}: {e}")
                response_to_user = f"Sorry, there was an error trying to {tool_name.replace('_', ' ')}. Please try again."
                updated_history = conversation_history + f"\nUser: {user_message}\nAssistant: {response_to_user}" 
                return response_to_user, updated_history
        else:
            
            print(f"ERROR: LLM specified an unknown tool: {tool_name}")
            response_to_user = "Sorry, I tried to use a tool I don't recognize. Please rephrase your request."
            updated_history = conversation_history + f"\nUser: {user_message}\nAssistant: {response_to_user}" 
            return response_to_user, updated_history

    elif direct_response:
        response_to_user = direct_response
        updated_history = conversation_history + f"\nUser: {user_message}\nAssistant: {response_to_user}" 
        return response_to_user, updated_history
    else:
      print(f"ERROR: Unhandled state after LLM response parsing. tool_name='{tool_name}', direct_response='{direct_response}'. Raw: '{llm_response_raw}'")
      response_to_user = "Sorry, an unexpected error occurred while processing the response."
      updated_history = conversation_history + f"\nUser: {user_message}\nAssistant: {response_to_user}" 
      return response_to_user, updated_history
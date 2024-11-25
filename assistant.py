from model import generate_response, fine_tune_model, apply_lora_optimization, load_improved_model
from system_commands import open_application, close_application, list_directory
from internet_fetch import fetch_live_data

# Runtime feedback log for collecting improvements
feedback_log = []


def collect_feedback(user_prompt, model_response, correct_response):
    """
    Collect interaction feedback for use in improvements.
    """
    return {
        "input_text": f"User: {user_prompt}\nAssistant: {model_response}",
        "expected_output": correct_response
    }


def interpret_and_execute(input_text):
    """
    Interpret and execute the user's command.
    """
    input_text = input_text.lower()

    # Handle web search-like behavior
    if "find information about" in input_text:
        topic = input_text.replace("find information about", "").strip()
        url = f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}"
        live_data = fetch_live_data(url)
        return generate_response(f"Summarize information about {topic}", live_data)

    # Handle direct URL access
    elif "access url" in input_text:
        url = input_text.replace("access url", "").strip()
        live_data = fetch_live_data(url)
        return generate_response(f"Process data from the URL: {url}", live_data)

    # Handle system commands
    elif "open" in input_text:
        app_name = input_text.replace("open", "").strip()
        return open_application(app_name)

    elif "close" in input_text:
        app_name = input_text.replace("close", "").strip()
        return close_application(app_name)

    elif "list files" in input_text:
        directory = input_text.replace("list files", "").strip()
        return list_directory(directory or ".")

    # Fallback to GPT-Neo for general queries
    else:
        return generate_response(input_text)


# Main Assistant Loop
if __name__ == "__main__":
    print("Assistant ready! Type 'exit' to quit.")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        
        response = interpret_and_execute(user_input)

        # Collect runtime feedback for improvements
        print(f"Assistant: {response}")
        improve = input("Do you want to improve this response? (yes/no): ").strip().lower()
        if improve == "yes":
            correct_response = input("What should have been the response? ")
            feedback_log.append(
                collect_feedback(user_prompt=user_input, model_response=response, correct_response=correct_response)
            )
            print("Feedback logged for future improvements.")

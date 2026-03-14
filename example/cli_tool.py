import os
import sys
import queue

# Adjust path to find the backend folder if running from examples/
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.browser_bridge import AIStudioBridge

def main():
    print("--- AI Studio Bridge CLI Controller ---")
    
    # 1. Instantiate the bridge
    bridge = AIStudioBridge()
    
    # 2. Start the bridge
    bridge.start()

    while True:
        print("\nOptions:")
        print("1. List Models")
        print("2. Set Active Model")
        print("3. Send Prompt (Chat)")
        print("4. Upload File & Extract")
        print("5. Reset Chat")
        print("6. Exit")
        
        choice = input("Select an option (1-6): ")

        if choice == "1":
            models = bridge.get_available_models()
            print(f"\nAvailable Models: {models}")

        elif choice == "2":
            model_name = input("Enter exact model name to switch to: ")
            success = bridge.set_model(model_name)
            print(f"Switch status: {success}")

        elif choice == "3":
            prompt = input("Enter your prompt: ")
            response = bridge.send_prompt(prompt, new_chat=False)
            print(f"\n--- AI Response ---\n{response}\n-------------------")

        elif choice == "4":
            file_path = input("Enter full path to file: ")
            if not os.path.exists(file_path):
                print("Error: File not found.")
                continue
            
            prompt = input("Enter extraction prompt: ")
            
            # Using the direct queue injection you wrote
            res_q = queue.Queue()
            bridge.cmd_queue.put(("upload_extract", (file_path, prompt), res_q))
            result = res_q.get(timeout=300)
            print(f"\n--- Extraction Result ---\n{result}\n-------------------------")

        elif choice == "5":
            bridge.reset()
            print("Chat reset.")

        elif choice == "6":
            print("Exiting...")
            break

if __name__ == "__main__":
    main()
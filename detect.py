from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
import ollama


def wait_for_file(file_path, timeout=5):
    """Wait until the file is fully written before processing."""
    initial_size = -1
    for _ in range(timeout):
        current_size = os.path.getsize(file_path)
        if current_size == initial_size:
            return True
        initial_size = current_size
        time.sleep(1)
    return False


class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        """Handle new image files detected in the monitored folder."""
        if not event.is_directory and event.src_path.endswith(('.png', '.jpg', '.jpeg')):
            full_path = event.src_path
            filename = os.path.basename(full_path)
            print(f"New file detected: {filename}")

            if wait_for_file(full_path):
                try:
                    response = ollama.chat(
                        model='llama3.2-vision',
                        messages=[{
                            'role': 'user',
                            'content': 'Act as an assistant for me and act as if I am blind. '
                                       'The dist value is the distance from the blind person to the object. '
                                       'Tell me all the objects in the image. Your response should only include the format '
                                       'object: distance and direction (right, left, front only) for all the objects in the frame, '
                                       'and don’t include any markdown or anything else.',
                            'images': [full_path]
                        }]
                    )

                    # Save the response to a file
                    with open(f"./responds/sharpest_frame.txt", "w") as text_file:
                        text_file.write(response.message.content)

                    # Optionally remove the processed file
                    os.system('rm ./inputs/sharpest_frame.png')

                    print(f"Ollama Response: {response.message.content}")
                except Exception as e:
                    print(f"Error sending file to Ollama: {e}")
            else:
                print(f"File {filename} is not stable. Skipping.")


folder_to_monitor = "/home/ubuntu/meta_llama_hacks/inputs"

event_handler = NewFileHandler()
observer = Observer()

observer.schedule(event_handler, folder_to_monitor, recursive=False)
observer.start()

print(f"Monitoring folder: {folder_to_monitor}")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()

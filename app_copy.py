
import ollama


response = ollama.chat(
                            model='llama3.2-vision',
                            messages=[{
                                'role': 'user',
                                'content': 'Act as an assistant for me and act as if I am blind. \
                                            The dist value is the distance from the blind person to the object. Tell me all the objects in the image \
                                            Your response should only include the format object: distance and direction \
                                            for all the objects in the frame and dont include any markdown only the text and dont include anything else.',                                    
                                'images': ['/home/ubuntu/meta_llama_hacks/inputs_old/images.jpeg']
                            }],
                        )

print(response)
print(response.message.content)
# with open("test.txt", "w") as f:
#     f.write(response.message.content)
    
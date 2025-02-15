from typing import List, Generator
import time

def stream_speech_buffer(speeches: List[str], buffer_size: int = 512, delay: float = 0.1) -> Generator[str, None, None]:
    """
    Stream speeches through a fixed-size buffer.
    
    Args:
        speeches (List[str]): List of speech texts to stream
        buffer_size (int): Size of each buffer chunk in bytes
        delay (float): Delay between buffer chunks in seconds
    
    Yields:
        str: Buffer chunks of the speech
    """
    for speech_idx, speech in enumerate(speeches, 1):
        # Convert speech to bytes
        speech_bytes = speech.encode('utf-8')
        
        # Calculate number of chunks needed
        num_chunks = (len(speech_bytes) + buffer_size - 1) // buffer_size
        
        print(f"\nProcessing Speech {speech_idx}/{len(speeches)}")
        print(f"Total bytes: {len(speech_bytes)}")
        print(f"Number of chunks: {num_chunks}")
        
        # Process speech in buffer-sized chunks
        for i in range(0, len(speech_bytes), buffer_size):
            chunk = speech_bytes[i:i + buffer_size]
            
            # Convert chunk back to string for processing
            chunk_text = chunk.decode('utf-8', errors='ignore')
            
            # Simulate processing delay
            time.sleep(delay)
            
            yield {
                'speech_number': speech_idx,
                'chunk_number': (i // buffer_size) + 1,
                'total_chunks': num_chunks,
                'chunk_size': len(chunk),
                'content': chunk_text
            }

# Example usage
def test_speech_streaming():
    # Sample speeches (you would replace these with your actual speeches)
    speeches = read_speeches_from_file('doctor-patient-dialogues.md')
    
    # Stream the speeches through the buffer
    for chunk_data in stream_speech_buffer(speeches):
        print("\nChunk Information:")
        print(f"Speech: {chunk_data['speech_number']}/{len(speeches)}")
        print(f"Chunk: {chunk_data['chunk_number']}/{chunk_data['total_chunks']}")
        print(f"Size: {chunk_data['chunk_size']} bytes")
        print(f"Content: {chunk_data['content']}...")

def read_speeches_from_file(file_path: str) -> list[str]:
    """
    Read speeches from a text file and return them as a list of strings.
    Each speech is assumed to be separated by a blank line.
    
    Args:
        file_path (str): Path to the file containing the speeches
        
    Returns:
        list[str]: List of speeches, each as a string
    """
    speeches = []
    current_speech = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Remove leading/trailing whitespace
                line = line.strip()
                
                # If we encounter a numbered line (e.g., "1.", "2."), it's a new speech
                if line and any(f"{i}." in line[:4] for i in range(1, 13)):
                    # If we have collected lines for a previous speech, add it
                    if current_speech:
                        speeches.append(' '.join(current_speech))
                        current_speech = []
                    # Start collecting the new speech, excluding the number
                    current_speech.append(line[line.find('.') + 1:].strip())
                # Add non-empty lines to current speech
                elif line:
                    current_speech.append(line)
            
            # Add the last speech if there is one
            if current_speech:
                speeches.append(' '.join(current_speech))
    
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return []
    
    # Remove any empty speeches
    speeches = [speech.strip() for speech in speeches if speech.strip()]
    
    print(f"Successfully loaded {len(speeches)} speeches")
    return speeches

def write_speeches_to_file(speeches: list[str], output_file: str):
    """
    Write speeches to a text file with proper formatting.
    
    Args:
        speeches (list[str]): List of speeches to write
        output_file (str): Path to the output file
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            for i, speech in enumerate(speeches, 1):
                file.write(f"{i}. {speech}\n\n")
        print(f"Successfully wrote {len(speeches)} speeches to {output_file}")
    except Exception as e:
        print(f"Error writing to file: {str(e)}")

if __name__ == "__main__":
    test_speech_streaming()
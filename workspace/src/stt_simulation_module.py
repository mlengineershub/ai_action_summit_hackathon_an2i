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
    speeches = [
        "Doctor, I've been experiencing this persistent lower back pain for about three months now...",
        "Based on your lab results and symptoms, I need to inform you that you have Type 2 diabetes...",
        # ... add more speeches as needed
    ]
    
    # Stream the speeches through the buffer
    for chunk_data in stream_speech_buffer(speeches):
        print("\nChunk Information:")
        print(f"Speech: {chunk_data['speech_number']}/{len(speeches)}")
        print(f"Chunk: {chunk_data['chunk_number']}/{chunk_data['total_chunks']}")
        print(f"Size: {chunk_data['chunk_size']} bytes")
        print(f"Content: {chunk_data['content'][:50]}...")  # Show first 50 chars of chunk

if __name__ == "__main__":
    test_speech_streaming()
from typing import List, Generator, Dict, Any
import time
import json

def stream_speech_buffer(
    speeches: List[Dict[str, Any]], buffer_size: int = 512, delay: float = 0.1
) -> Generator[Dict[str, Any], None, None]:
    """Streams speeches in chunks with a buffer."""
    for speech_idx, speech in enumerate(speeches, 1):
        speech_text = speech.get("text", "")  # Change "content" to "text"
        
        # Debug: Print the speech content to check if it's empty or malformed
        print(f"Speech {speech_idx} content: {repr(speech_text)}")

        if not speech_text:  # If content is empty or None
            print(f"Warning: Speech {speech_idx} has no content.")
            continue  # Skip this speech and move to the next

        speech_bytes = speech_text.encode("utf-8")
        num_chunks = (len(speech_bytes) + buffer_size - 1) // buffer_size

        print(f"\nProcessing Speech {speech_idx}/{len(speeches)}")
        print(f"Total bytes: {len(speech_bytes)}")
        print(f"Number of chunks: {num_chunks}")

        for i in range(0, len(speech_bytes), buffer_size):
            chunk = speech_bytes[i : i + buffer_size]
            chunk_text = chunk.decode("utf-8", errors="ignore")
            time.sleep(delay)

            yield {
                "speech_number": speech_idx,
                "chunk_number": (i // buffer_size) + 1,
                "total_chunks": num_chunks,
                "chunk_size": len(chunk),
                "content": chunk_text,
            }

def test_speech_streaming() -> None:
    """..."""
    speeches = read_speeches_from_json("doctor-patient-dialogues.json")
    for chunk_data in stream_speech_buffer(speeches):
        print("\nChunk Information:")
        print(f"Speech: {chunk_data['speech_number']}/{len(speeches)}")
        print(f"Chunk: {chunk_data['chunk_number']}/{chunk_data['total_chunks']}")
        print(f"Size: {chunk_data['chunk_size']} bytes")
        print(f"Content: {chunk_data['content']}")

def read_speeches_from_json(file_path: str) -> List[Dict[str, Any]]:
    """Reads speeches from a JSON file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                speeches = data
            else:
                speeches = data.get("speeches", [])
            print(f"Successfully loaded {len(speeches)} speeches from {file_path}")
            return speeches
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []
    except Exception as e:
        print(f"Error reading JSON file: {str(e)}")
        return []

def write_speeches_to_file(speeches: List[Dict[str, Any]], output_file: str) -> None:
    """..."""
    try:
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(speeches, file, indent=4)
        print(f"Successfully wrote {len(speeches)} speeches to {output_file}")
    except Exception as e:
        print(f"Error writing to file: {str(e)}")

if __name__ == "__main__":
    test_speech_streaming()

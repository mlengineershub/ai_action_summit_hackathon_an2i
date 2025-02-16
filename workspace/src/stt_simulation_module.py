from typing import List, Generator, Dict, Any
import time

def stream_speech_buffer(
    speeches: List[str], buffer_size: int = 512, delay: float = 0.1
) -> Generator[Dict[str, Any], None, None]:
    """
    Streams speeches through a fixed-size buffer, yielding chunks of the speech with metadata.

    Args:
        speeches (List[str]): A list of speech texts to be streamed.
        buffer_size (int, optional): The size of each buffer chunk in bytes. Defaults to 512.
        delay (float, optional): Delay time in seconds between yielding each chunk. Defaults to 0.1.

    Yields:
        Dict[str, Any]: A dictionary containing:
            - 'speech_number': Index of the current speech.
            - 'chunk_number': Index of the current chunk.
            - 'total_chunks': Total number of chunks in the speech.
            - 'chunk_size': Size of the current chunk in bytes.
            - 'content': Text content of the current chunk.
    """
    for speech_idx, speech in enumerate(speeches, 1):
        speech_bytes = speech.encode("utf-8")
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
    """Tests the speech streaming by reading speeches from a file and streaming them."""
    speeches = read_speeches_from_file("doctor-patient-dialogues.md")
    for chunk_data in stream_speech_buffer(speeches):
        print("\nChunk Information:")
        print(f"Speech: {chunk_data['speech_number']}/{len(speeches)}")
        print(f"Chunk: {chunk_data['chunk_number']}/{chunk_data['total_chunks']}")
        print(f"Size: {chunk_data['chunk_size']} bytes")
        print(f"Content: {chunk_data['content']}...")

def read_speeches_from_file(file_path: str) -> List[str]:
    """
    Reads speeches from a specified text file, identifying and splitting speeches by numbered sections.

    Args:
        file_path (str): Path to the file containing speeches.

    Returns:
        List[str]: A list of extracted speech texts.
    """
    speeches = []
    current_speech = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line and any(f"{i}." in line[:4] for i in range(1, 13)):
                    if current_speech:
                        speeches.append(" ".join(current_speech))
                        current_speech = []
                    current_speech.append(line[line.find(".") + 1 :].strip())
                elif line:
                    current_speech.append(line)
            if current_speech:
                speeches.append(" ".join(current_speech))
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return []
    speeches = [speech.strip() for speech in speeches if speech.strip()]
    print(f"Successfully loaded {len(speeches)} speeches")
    return speeches

def write_speeches_to_file(speeches: List[str], output_file: str) -> None:
    """
    Writes speeches to a specified output file, numbering each speech.

    Args:
        speeches (List[str]): A list of speeches to write.
        output_file (str): Path to the output file.
    """
    try:
        with open(output_file, "w", encoding="utf-8") as file:
            for i, speech in enumerate(speeches, 1):
                file.write(f"{i}. {speech}\n\n")
        print(f"Successfully wrote {len(speeches)} speeches to {output_file}")
    except Exception as e:
        print(f"Error writing to file: {str(e)}")

if __name__ == "__main__":
    test_speech_streaming()

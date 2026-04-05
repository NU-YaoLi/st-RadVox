from openai import OpenAI
import tempfile
import os
import re
from pydub import AudioSegment
import io

def process_audio(api_key, audio_bytes, model_choice):
    client = OpenAI(api_key=api_key)
    
    # 1. Convert WAV bytes to high-quality MP3 (320 kbps)
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="wav")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        audio.export(temp_audio.name, format="mp3", bitrate="320k")
        temp_audio_path = temp_audio.name

    try:
        with open(temp_audio_path, "rb") as audio_file:
            # Use the model selected by the user
            transcript_response = client.audio.transcriptions.create(
                model=model_choice, 
                file=audio_file
            )

        raw_transcription = transcript_response.text
        
        # Replace spoken "next line" (case-insensitive, ignoring surrounding punctuation/spaces) with actual \n
        transcription = re.sub(r'(?i)[,\.]?\s*next line[,\.]?\s*', '\n', raw_transcription)
        
        # 2. Process text for two versions
        prompt = f"""
        You are an expert veterinary radiologist scribe. 
        Take the following transcribed medical dictation and provide two rewritten versions:
        
        1. [Grammar Corrected Version]: Fix ONLY grammar&spelling mistakes and hiccups in user's voice input. Do not rephrase the content or change the original wording. You MUST preserve all newlines and structural formatting exactly as provided.
        2. [Professional Version]: A highly polished, professional clinical version suitable for official veterinary radiology records or doctor-to-doctor communication. Rephrase into a professional clinical tone. You MUST preserve all newlines and structural formatting from the original text. Regarding the content output format, use a double line break (\n\n) to create an empty line between the description and the impressions.
        
        CRITICAL FORMATTING RULE FOR BOTH VERSIONS: All continuous adjectives in the sentences must be separated by commas.
        Example Input: "An ill-defined roughly triangular cranioventral thoracic soft tissueopacity on the lateral projections is most consistent with thymic tissue/thymicremnant in a young patient."
        Example Output: "An ill-defined, roughly, triangular, cranioventral, thoracic, soft tissueopacity on the lateral projections is most consistent with thymic tissue/thymicremnant in a young patient."
        
        Use the exact headings "[Grammar Corrected Version]" and "[Professional Version]" to separate your response.
        
        Transcribed Text:
        "{transcription}"
        """
        
        chat_response = client.chat.completions.create(
            model="gpt-4o", # Updated this to gpt-4o as gpt-5.4 doesn't exist yet, but you can change it back if you have a custom deployment
            messages=[
                {"role": "system", "content": "You are an expert veterinary radiologist."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        polished_text = chat_response.choices[0].message.content
        
        # Parse the two versions out of the response
        parts = polished_text.split("[Professional Version]")
        grammar_text = parts[0].replace("[Grammar Corrected Version]", "").strip()
        pro_text = parts[1].strip() if len(parts) > 1 else "Could not generate professional version."
        
        return transcription, grammar_text, pro_text

    finally:
        # Clean up the temporary file
        os.remove(temp_audio_path)
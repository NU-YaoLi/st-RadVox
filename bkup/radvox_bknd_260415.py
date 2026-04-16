import os
import re
import tempfile
import subprocess
from openai import OpenAI

def process_audio(api_key, audio_bytes, model_choice):
    client = OpenAI(api_key=api_key)
    
    # 1. Convert WAV bytes to high-quality MP3 (320 kbps) using native subprocess
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
        temp_wav.write(audio_bytes)
        temp_wav_path = temp_wav.name

    temp_mp3_path = temp_wav_path.replace(".wav", ".mp3")

    try:
        # Execute ffmpeg command line via Python 3.14+ subprocess standard practice
        subprocess.run([
            "ffmpeg", "-y", "-i", temp_wav_path, 
            "-b:a", "320k", temp_mp3_path
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        with open(temp_mp3_path, "rb") as audio_file:
            # Use the model selected by the user
            transcript_response = client.audio.transcriptions.create(
                model=model_choice, 
                file=audio_file
            )

        raw_transcription = transcript_response.text
        
        # Replace spoken "next line" (case-insensitive, ignoring surrounding punctuation/spaces) with actual \n
        transcription = re.sub(r'(?i)[,\.]?\s*next line[,\.]?\s*', '\n', raw_transcription)
        
        # 2. First API Call: Professional Clinical Version
        prompt_pro = f"""
        You are an expert veterinary radiologist scribe. 
        Take the following transcribed medical dictation and provide a highly polished, professional clinical version suitable for official veterinary radiology records or doctor-to-doctor communication. 
        Rephrase into a professional clinical tone. You MUST preserve all newlines and structural formatting from the original text. Regarding the content output format, use a double line break (\\n\\n) to create an empty line between the description and the impressions.
        
        CRITICAL INSTRUCTION: Ensure that any continuous adjectives in a sentence are strictly separated by a comma. 
        For example: "An ill-defined roughly triangular cranioventral thoracic soft tissue opacity" MUST be written as "An ill-defined, roughly, triangular, cranioventral, thoracic, soft tissue opacity".
        
        Transcribed Text:
        "{transcription}"
        """
        
        chat_response_pro = client.chat.completions.create(
            model="gpt-5.4",
            messages=[
                {"role": "system", "content": "You are an expert veterinary radiologist."},
                {"role": "user", "content": prompt_pro}
            ],
            temperature=0.3
        )
        
        pro_text = chat_response_pro.choices[0].message.content.strip()

        # 3. Second API Call: Radiology Report Version
        prompt_report = f"""
        You are an expert veterinary radiologist. 
        Take the following professional clinical text and format it into a structured Radiology Report. 
        
        CRITICAL INSTRUCTIONS:
        1. Focus ONLY on two sections: "Diagnostic Interpretation" and "Conclusions". Omit all other parts (such as patient history, study details, etc.).
        2. Infer the body parts being discussed (e.g., Head, Thorax, Abdomen, Musculoskeletal) from the text.
        3. Categorize the findings under these body parts.
        4. The output MUST exactly follow the formatting structure below.
        5. Ensure to use Oxford comma to seperate any continuous adjectives in a sentence.

        Diagnostic Interpretation
        [Body Part 1]: [Paragraph description of findings]
        [Body Part 2]: [Paragraph description of findings]

        Conclusions
        [Body Part 1]:
        * [Bullet point 1]
        * [Bullet point 2]
        [Body Part 2]:
        * [Bullet point 1]

        Professional Clinical Text to format:
        "{pro_text}"
        """

        chat_response_report = client.chat.completions.create(
            model="gpt-5.4",
            messages=[
                {"role": "system", "content": "You are an expert veterinary radiologist."},
                {"role": "user", "content": prompt_report}
            ],
            temperature=0.2
        )

        report_text = chat_response_report.choices[0].message.content.strip()
        
        return transcription, pro_text, report_text

    finally:
        # Clean up the temporary files
        os.remove(temp_wav_path)
        if os.path.exists(temp_mp3_path):
            os.remove(temp_mp3_path)
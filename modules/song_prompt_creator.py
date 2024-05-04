from openai import OpenAI
import os
import getpass

def create_song_prompt(query, image_descriptions, openai_client):
    """
    Creates a song prompt from a query and image descriptions.
    """
    prompt = f"Say the key words for the  genres and instruments of a song based on the query '{query}' and the following image descriptions:\n"
    for image_description in image_descriptions:
        prompt += f"Image Description: {image_description}\n"
    ans = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": """
                   Say the genre and characteristics of a song based on the query 'Happy' and the following image descriptions:
                   A beautiful sunset over the ocean
                   A sailboat on the water
                   A beach with palm trees
                   """},
                {"role": "system", "content": "Relaxing, calm, peacefull, Guitar, piano, Slow tempo"},
                {"role": "user", "content": prompt},
        ]
    )
    
    return ans.choices[0].message.content
    
if __name__ == '__main__':
    if not os.environ.get("OPENAI_API_KEY"): 
        os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
    openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    query = "Sadness"
    image_descriptions = ["Long winter nights", "A lonely person", "A rainy day"]
    print(create_song_prompt(query, image_descriptions, openai_client))
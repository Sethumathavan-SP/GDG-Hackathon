API_KEY = 'AIzaSyDTrzcaUzOX5XQvpf6JGByPNOzXtsEj3dg'

prompt = '''
        don't adress patient name and your sincerely organization name
        add heading to all three sections
        Disclaimer: This is an AI-generated preliminary report and should not be considered a final diagnosis. A doctor will review your case and provide expert guidance soon."

Based on the provided medical image, generate a clear and supportive report for the patient with the following details:

Most Likely Condition (with Confidence Percentage):

Clearly state the most likely condition, followed by the estimated confidence percentage (e.g., "Based on the image provided, the most likely condition is allergic contact dermatitis with a x% confidence level"). Ensure the language is reassuring but transparent.
Add a note explaining that a definitive diagnosis requires a doctor’s review and examination, as the image can only provide an initial indication.
Precautionary Measures:

Provide simple and actionable advice for the patient, like: “Avoid scratching the affected area, keep the skin moisturized, and avoid any known allergens.”
Next Steps:

Reassure the patient that a doctor will review the condition soon and offer further guidance: “Please reach out to your doctor for a thorough consultation and treatment plan. They will be able to confirm the diagnosis and offer appropriate treatment.”
The tone should be warm, confident, and compassionate, emphasizing that while this is an educated guess, the final diagnosis will be confirmed by a healthcare professional.'''


import google.generativeai as genai
from IPython.display import clear_output, display, Markdown

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(model_name='gemini-1.5-flash')

def analyze(img): 
        response = model.generate_content([prompt, img], stream=False)
        return response.text

def get_keyword(AI_report):
        response = model.generate_content([f"giveme only the disease from this report nothing else: \"{AI_report}\""], stream=False)
        return response.text

def severity_score(data,curr_disease):
        Docter_prompt = f'''
                        "Based on the data from {data}, assign a severity score between 1.0 and 10.0 for {curr_disease}. Return only the floating-point number with no additional text.if no the data is empty give a initial siverity value. remeber only give a floating number no other text code or anything"
                '''
        response = model.generate_content(Docter_prompt)
        print(response.text)
        return response.text
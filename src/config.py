# config.py
DATA_PATH = r'D:\Autism-Spectrum-Disorder--Medical-Analyisis\datasets'
QCHAT_THRESHOLD = 4
FEATURE_COLS = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'Jaundice', 'Family_mem_with_ASD', 'Age_Mons']
QUESTIONS = [
    "1. Does your child look at you when you call his/her name?",
    "2. How easy is it for you to get eye contact with your child?",
    "3. Does your child point to indicate that he or she wants something?",
    "4. Does your child point to share interest with you?",
    "5. Does your child pretend?",
    "6. Does your child follow where you’re looking?",
    "7. If someone is visibly upset, does your child show signs of wanting to comfort them?",
    "8. Does your child respond when asked to repeat a word?",
    "9. Does your child use simple gestures?",
    "10. Does your child stare at nothing with no apparent purpose?"
]
OPTIONS = ['Always', 'Usually', 'Sometimes', 'Rarely', 'Never']
image1 = r'static/images/asd1.webp'
image2 = r'static/images/asd2.jpg'
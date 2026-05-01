from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

MODEL_NAME = "Qwen/Qwen2-0.5B-Instruct"

print("Loading AI model... please wait")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=200,
    do_sample=True,
    temperature=0.7
)

print("AI Model Loaded ✅")


def ask_ai(question: str):
    q = question.lower().strip()

    # greetings fix
    if q in ["hi", "hello", "hey"]:
        return "Hello! How can I help you today?"

    if q in ["how are you", "how are you?"]:
        return "I'm doing well! How can I help you today?"

    if q in ["good morning"]:
        return "Good morning! Hope you have a great day."

    if q in ["good evening"]:
        return "Good evening! How can I assist you?"

    if q in ["how was the day", "how was your day"]:
        return "My day has been great. Thanks for asking! How was yours?"

    # normal AI response
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. Give clear short answers."
        },
        {
            "role": "user",
            "content": question
        }
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(text, return_tensors="pt")

    outputs = model.generate(
        **inputs,
        max_new_tokens=120,
        temperature=0.5,
        do_sample=True,
        top_p=0.9
    )

    result = tokenizer.decode(outputs[0], skip_special_tokens=True)

    answer = result.split("assistant")[-1].strip()

    return answer
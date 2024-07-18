import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
import dotenv 
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
dotenv.load_dotenv()
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

model_id = "allganize/Llama-3-Alpha-Ko-8B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id)
llm = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype="auto",
    device_map="auto",
)


prompt = PromptTemplate.from_template("""|begin_of_text|><|start_header_id|>system<|end_header_id|>
        너는 user 질문에 정보의 내용대로 답하는 assistant야. user가 질문하는 내용을 정보를 이용해서 정확하고 최대한 자세하게 답해. 질문 내용에 대답할 수 없으면 '이 질문은 답변할 수 없습니다'라고 답해. 한국어(Korean)로 대답해.
        <|eot_id|><|start_header_id|>user<|end_header_id|>
        ### 질문: {question}
        ### 답변:
        """)


def generate_response(question):
    prompt_text = prompt.format(question=question)
    input_ids = tokenizer(prompt_text, return_tensors="pt").input_ids.to(llm.device)
    
    # Generate response
    outputs = llm.generate(
        input_ids,
        max_new_tokens=2048,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.pad_token_id,
        do_sample=True,
        temperature=0.1,
        top_p=0.9,

    )
    response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response_text.split("system")[2].replace("\n         ","")




#Event handler for Slack
@app.event("app_mention")
def handle_app_mention_events(body, say, logger):
    message = body["event"]['text']
    response = generate_response(message)
    say(response)

#Message handler for Slack
@app.message(".*")
def message_handler(message, say, logger):
    output = generate_response(message['text'])
    say(output)
    
# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
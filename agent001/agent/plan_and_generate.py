import json
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from agent.prompts import CODE_GENERATION_PROMPT
from utils.helpers import write_files, load_ticket
from langchain.callbacks import StdOutCallbackHandler
from langchain_arize import ArizeCallbackHandler  # Install via `pip install langchain-arize`

def run_agent(ticket_path: str):
    # Load the ticket
    ticket = load_ticket(ticket_path)

    # Initialize LLM and chain
    llm = ChatOpenAI(temperature=0.2)
    arize_handler = ArizeCallbackHandler(space_key=\"YOUR_ARIZE_SPACE_KEY\", api_key=\"YOUR_API_KEY\")
    chain = LLMChain(
        llm=llm,
        prompt=CODE_GENERATION_PROMPT,
        callbacks=[StdOutCallbackHandler(), arize_handler]
    )

    # Run the chain
    response = chain.run({
        \"ticket_id\": ticket[\"id\"],
        \"title\": ticket[\"title\"],
        \"description\": ticket[\"description\"],
        \"acceptance_criteria\": \"\\n\".join(ticket[\"acceptance_criteria\"])
    })

    # Parse the generated JSON code
    generated_files = json.loads(response)
    write_files(generated_files, \"generated_code\")

    print(\"✅ Code generation complete.\")
    return generated_files
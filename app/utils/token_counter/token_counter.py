from typing import Union, List
import tiktoken

def approximate_count_tokens(messages: Union[str,List[dict]],
                             model_name: str = "gpt-3.5-turbo") -> int:
    # Load the tokenizer for the selected model
    encoding = tiktoken.encoding_for_model(model_name)

    # Tokenize and count tokens
    if isinstance(messages, str):
        return len(encoding.encode(messages))

    if model_name == "gpt-3.5-turbo":
        tokens_per_message = 4  # Every message adds 4 tokens
        tokens_per_name = -1  # If 'name' field is present, subtract 1
    elif model_name == "gpt-4":
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        raise NotImplementedError(f"Token counting for model {model_name} not implemented.")

    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # Every reply ends with <|assistant|>
    return num_tokens



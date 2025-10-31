# prompt_sandbox.py (Complete Code with New Test)
from rag_utils import PROMPTS

def build_prompt(strategy, context, question):
    #if we do not find the strategy then we will use the template for tot(Tree-of-thought).
    tmpl = PROMPTS.get(strategy, PROMPTS["tot"]) 
    return tmpl.format(context=context, question=question)
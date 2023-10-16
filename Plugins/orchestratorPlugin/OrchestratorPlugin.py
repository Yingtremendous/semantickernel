import json
from tkinter import Variable

from matplotlib.pyplot import cla
from semantic_kernel import ContextVariables, kernel
from semantic_kernel.skill_defintion import sk_function, sk_function_context_parameter
from semantic_kernel.orchestration.sk_context import SKContext


class Orchestrator:
    # this plugin runs other function
    # pass kernel into the constructor
    def __init__(self, kernel: kernel):
        self._kernel = kernel
    @sk_function(
    description="Routes the request to the appropriate function",
    name="RouteRequest")
    async def route_request(self, context: SKContext) -> str:
        # save ori request
        request = context["input"]
        
        # add a list of variables
        variables = ContextVariables()
        variables["input"] = request
        variables["options"] = "Sqrt,Multiply"

        # retrieve intent from request
        get_intent = self._kernel.skills.get_function("OrchestratorPlugin", "GetIntent")
        intent = await self._kernel.run_async(get_intent, variables)
        intent = intent.result.strip()

        get_numbers = self._kernel.skills.get_function("OrchestratorPlugin", "GetNumbers")  
        getNumberContext = await self._kernel.run_async(get_numbers, request).result
        numbers = json.loads(getNumberContext)
        # call the appropriate function
        if intent == "Sqrt":
            sqrt = self._kernel.skills.get_function("MathPlugin", "Sqrt")
            result = await self._kernel.run_async(sqrt, input_str=numbers["number1"])
            return result.result
        elif intent == "Multiply":
            multiply = self._kernel.skills.get_function("MathPlugin", "Multiply")
            variables = ContextVariables()
            variables["input"] = numbers["number1"]
            variables["number2"] = numbers["number2"]   
            result = await self._kernel.run_async(multiply,input_vars=variables)
            return result["input"]
        else:
            return "I'm sorry, I don't know how to do that."